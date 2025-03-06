import click
import subprocess

@click.group()
def main():
    """Health Intervention Predictor CLI"""
    pass

@main.command()
def update_requirements():
    """Update installed packages from requirements.txt"""
    click.echo("Updating packages from requirements.txt...")
    subprocess.run(["pip", "install", "--upgrade", "-r", "requirements.txt"], check=True)
    click.echo("Update completed.")

if __name__ == "__main__":
    main()
