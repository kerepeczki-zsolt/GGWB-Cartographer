import torch
import torch.nn as nn
import torch.nn.functional as F
class BetaVAE(nn.Module):
    def __init__(self, latent_dim=32, beta=4.0, input_shape=(1, 128, 128)):
        super().__init__()
        self.latent_dim, self.beta, self.input_shape = latent_dim, beta, input_shape
        c, h, w = input_shape
        flat_dim = c * h * w
        self.encoder = nn.Sequential(nn.Flatten(), nn.Linear(flat_dim, 512), nn.ReLU(), nn.Linear(512, latent_dim * 2))
        self.decoder = nn.Sequential(nn.Linear(latent_dim, 512), nn.ReLU(), nn.Linear(512, flat_dim), nn.Sigmoid())
    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        return mu + torch.randn_like(std) * std
    def forward(self, x):
        batch_size = x.size(0)
        mu, logvar = self.encoder(x).chunk(2, dim=1)
        z = self.reparameterize(mu, logvar)
        recon = self.decoder(z).view(batch_size, *self.input_shape)
        return recon, mu, logvar
    def loss_function(self, recon_x, x, mu, logvar):
        recon_loss = F.mse_loss(recon_x, x, reduction="mean")
        kl_loss = -0.5 * torch.mean(1 + logvar - mu.pow(2) - logvar.exp())
        return {"total_loss": recon_loss + self.beta * kl_loss, "recon_loss": recon_loss, "kl_loss": kl_loss}
