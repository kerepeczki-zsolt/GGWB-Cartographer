import sys
import os
# Kényszerítjük a FINAL mappát a keresőbe
sys.path.append("C:/Users/vivob/GGWB_FINAL_V12")

import torch
import torch.optim as optim
import numpy as np
from framework.models.beta_vae import BetaVAE, vae_loss_function

class TrainingEngine:
    def __init__(self, input_dim=2048, latent_dim=16, beta=4.0):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = BetaVAE(input_dim=input_dim, latent_dim=latent_dim, beta=beta).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=1e-3)
        self.beta = beta

    def train_step(self, data_batch):
        self.model.train()
        data = torch.FloatTensor(data_batch).to(self.device)
        self.optimizer.zero_grad()
        recon_batch, mu, logvar = self.model(data)
        loss = vae_loss_function(recon_batch, data, mu, logvar, self.beta)
        loss.backward()
        self.optimizer.step()
        return loss.item()

if __name__ == "__main__":
    engine = TrainingEngine()
    test_data = np.random.normal(0, 1, (16, 2048))
    loss = engine.train_step(test_data)
    print(f"[V12 SIKER] Motor aktiválva. Loss: {loss:.4f}")
