import torch; import sys; import os; sys.path.append(os.getcwd()); from framework.models.beta_vae import BetaVAE
def main():
    model = BetaVAE(latent_dim=32, beta=4.0, input_shape=(1, 128, 128))
    dummy_input = torch.randn(4, 1, 128, 128)
    recon, mu, logvar = model(dummy_input)
    losses = model.loss_function(recon, dummy_input, mu, logvar)
    losses["total_loss"].backward()
    print("Dummy test SUCCESS"); print("Total loss:", losses["total_loss"].item())
if __name__ == "__main__": main()
