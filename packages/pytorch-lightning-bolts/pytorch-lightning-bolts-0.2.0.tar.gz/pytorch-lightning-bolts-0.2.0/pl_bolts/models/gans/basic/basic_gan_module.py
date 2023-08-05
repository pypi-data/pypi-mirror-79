import os
from argparse import ArgumentParser

import torch
import pytorch_lightning as pl
from torch.nn import functional as F

from pl_bolts.datamodules import MNISTDataModule
from pl_bolts.models.gans.basic.components import Generator, Discriminator


class GAN(pl.LightningModule):

    def __init__(self,
                 datamodule: pl.LightningDataModule = None,
                 latent_dim: int = 32,
                 batch_size: int = 100,
                 learning_rate: float = 0.0002,
                 data_dir: str = '',
                 num_workers: int = 8,
                 **kwargs):
        """
        Vanilla GAN implementation.

        Example::

            from pl_bolts.models.gan import GAN

            m = GAN()
            Trainer(gpus=2).fit(m)

        Example CLI::

            # mnist
            python  basic_gan_module.py --gpus 1

            # imagenet
            python  basic_gan_module.py --gpus 1 --dataset 'imagenet2012'
            --data_dir /path/to/imagenet/folder/ --meta_dir ~/path/to/meta/bin/folder
            --batch_size 256 --learning_rate 0.0001

        Args:

            datamodule: the datamodule (train, val, test splits)
            latent_dim: emb dim for encoder
            batch_size: the batch size
            learning_rate: the learning rate
            data_dir: where to store data
            num_workers: data workers

        """
        super().__init__()

        # makes self.hparams under the hood and saves to ckpt
        self.save_hyperparameters()

        self._set_default_datamodule(datamodule)

        # networks
        self.generator = self.init_generator(self.img_dim)
        self.discriminator = self.init_discriminator(self.img_dim)

    def _set_default_datamodule(self, datamodule):
        # link default data
        if datamodule is None:
            datamodule = MNISTDataModule(
                data_dir=self.hparams.data_dir,
                num_workers=self.hparams.num_workers,
                normalize=True
            )
        self.datamodule = datamodule
        self.img_dim = self.datamodule.size()

    def init_generator(self, img_dim):
        generator = Generator(latent_dim=self.hparams.latent_dim, img_shape=img_dim)
        return generator

    def init_discriminator(self, img_dim):
        discriminator = Discriminator(img_shape=img_dim)
        return discriminator

    def forward(self, z):
        """
        Generates an image given input noise z

        Example::

            z = torch.rand(batch_size, latent_dim)
            gan = GAN.load_from_checkpoint(PATH)
            img = gan(z)
        """
        return self.generator(z)

    def generator_loss(self, x):
        # sample noise
        z = torch.randn(x.shape[0], self.hparams.latent_dim, device=self.device)
        y = torch.ones(x.size(0), 1, device=self.device)

        # generate images
        generated_imgs = self(z)

        D_output = self.discriminator(generated_imgs)

        # ground truth result (ie: all real)
        g_loss = F.binary_cross_entropy(D_output, y)

        return g_loss

    def discriminator_loss(self, x):
        # train discriminator on real
        b = x.size(0)
        x_real = x.view(b, -1)
        y_real = torch.ones(b, 1, device=self.device)

        # calculate real score
        D_output = self.discriminator(x_real)
        D_real_loss = F.binary_cross_entropy(D_output, y_real)

        # train discriminator on fake
        z = torch.randn(b, self.hparams.latent_dim, device=self.device)
        x_fake = self(z)
        y_fake = torch.zeros(b, 1, device=self.device)

        # calculate fake score
        D_output = self.discriminator(x_fake)
        D_fake_loss = F.binary_cross_entropy(D_output, y_fake)

        # gradient backprop & optimize ONLY D's parameters
        D_loss = D_real_loss + D_fake_loss

        return D_loss

    def training_step(self, batch, batch_idx, optimizer_idx):
        x, _ = batch

        # train generator
        result = None
        if optimizer_idx == 0:
            result = self.generator_step(x)

        # train discriminator
        if optimizer_idx == 1:
            result = self.discriminator_step(x)

        return result

    def generator_step(self, x):
        g_loss = self.generator_loss(x)

        # log to prog bar on each step AND for the full epoch
        # use the generator loss for checkpointing
        result = pl.TrainResult(minimize=g_loss, checkpoint_on=g_loss)
        result.log('g_loss', g_loss, on_epoch=True, prog_bar=True)
        return result

    def discriminator_step(self, x):
        # Measure discriminator's ability to classify real from generated samples
        d_loss = self.discriminator_loss(x)

        # log to prog bar on each step AND for the full epoch
        result = pl.TrainResult(minimize=d_loss)
        result.log('d_loss', d_loss, on_epoch=True, prog_bar=True)
        return result

    def configure_optimizers(self):
        lr = self.hparams.learning_rate

        opt_g = torch.optim.Adam(self.generator.parameters(), lr=lr)
        opt_d = torch.optim.Adam(self.discriminator.parameters(), lr=lr)
        return [opt_g, opt_d], []

    @staticmethod
    def add_model_specific_args(parent_parser):
        parser = ArgumentParser(parents=[parent_parser], add_help=False)
        parser.add_argument('--learning_rate', type=float, default=0.0002, help="adam: learning rate")
        parser.add_argument('--adam_b1', type=float, default=0.5,
                            help="adam: decay of first order momentum of gradient")
        parser.add_argument('--adam_b2', type=float, default=0.999,
                            help="adam: decay of first order momentum of gradient")
        parser.add_argument('--latent_dim', type=int, default=100,
                            help="generator embedding dim")
        parser.add_argument('--batch_size', type=int, default=64, help="size of the batches")
        parser.add_argument('--num_workers', type=int, default=8, help="num dataloader workers")
        parser.add_argument('--data_dir', type=str, default=os.getcwd())

        return parser


def cli_main():
    from pl_bolts.callbacks import LatentDimInterpolator, TensorboardGenerativeModelImageSampler
    from pl_bolts.datamodules import STL10DataModule, ImagenetDataModule

    pl.seed_everything(1234)

    parser = ArgumentParser()
    parser.add_argument('--dataset', type=str, default='mnist', help='mnist, stl10, imagenet2012')

    parser = pl.Trainer.add_argparse_args(parser)
    parser = GAN.add_model_specific_args(parser)
    parser = ImagenetDataModule.add_argparse_args(parser)
    args = parser.parse_args()

    # default is mnist
    datamodule = None
    if args.dataset == 'imagenet2012':
        datamodule = ImagenetDataModule.from_argparse_args(args)
    elif args.dataset == 'stl10':
        datamodule = STL10DataModule.from_argparse_args(args)

    gan = GAN(**vars(args), datamodule=datamodule)
    callbacks = [TensorboardGenerativeModelImageSampler(), LatentDimInterpolator()]

    trainer = pl.Trainer.from_argparse_args(
        args,
        callbacks=callbacks,
        progress_bar_refresh_rate=10
    )
    trainer.fit(gan)


if __name__ == '__main__':
    cli_main()
