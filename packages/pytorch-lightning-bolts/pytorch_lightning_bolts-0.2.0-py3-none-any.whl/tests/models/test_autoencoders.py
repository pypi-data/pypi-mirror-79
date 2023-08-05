import pytorch_lightning as pl
import torch
from pytorch_lightning import seed_everything

from pl_bolts.models.autoencoders import VAE, AE
from pl_bolts.models.autoencoders.basic_ae import AEEncoder
from pl_bolts.models.autoencoders.basic_vae import Encoder, Decoder


def test_vae(tmpdir):
    seed_everything()

    model = VAE(data_dir=tmpdir, batch_size=2, num_workers=0)
    trainer = pl.Trainer(fast_dev_run=True, default_root_dir=tmpdir, deterministic=True)
    trainer.fit(model)
    results = trainer.test(model)[0]
    loss = results['test_loss']

    assert loss > 0, 'VAE failed'


def test_ae(tmpdir):
    seed_everything()

    model = AE(data_dir=tmpdir, batch_size=2)
    trainer = pl.Trainer(fast_dev_run=True, default_root_dir=tmpdir)
    trainer.fit(model)
    trainer.test(model)


def test_basic_ae_encoder(tmpdir):
    seed_everything()

    hidden_dim = 128
    latent_dim = 2
    width = height = 28
    batch_size = 16
    channels = 1

    encoder = AEEncoder(hidden_dim, latent_dim, width, height)
    x = torch.randn(batch_size, channels, width, height)
    z = encoder(x)

    assert z.shape == (batch_size, latent_dim)


def test_basic_vae_components(tmpdir):
    seed_everything()

    hidden_dim = 128
    latent_dim = 2
    width = height = 28
    batch_size = 16
    channels = 1

    enc = Encoder(hidden_dim, latent_dim, channels, width, height)
    x = torch.randn(batch_size, channels, width, height)
    mu, sigma = enc(x)

    assert mu.shape == sigma.shape

    dec = Decoder(hidden_dim, latent_dim, width, height, channels)
    decoded_x = dec(mu)

    assert decoded_x.view(-1).shape == x.view(-1).shape
