import subprocess
import requests
import tarfile
import os


def download_and_extract_dentist(version='v4.0.0'):
    url = f"https://github.com/a-ludi/dentist/releases/download/{version}/dentist.{version}.x86_64.tar.gz"
    filename = url.split('/')[-1]
    filepath = f"/tmp/{filename}"

    # Download Dentist tar.gz
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filepath, 'wb') as f:
            f.write(response.raw.read())

        # Extract the tar.gz file
        with tarfile.open(filepath, 'r:gz') as tar:
            tar.extractall(path='/tmp/')

        print(f"Dentist version {version} downloaded and extracted.")
        return f"/tmp/dentist.{version}.x86_64"
    else:
        raise Exception(f"Error downloading Dentist: Status code {response.status_code}")


def setup_snakemake_workflow(workdir, dentist_dir):
    # Copy necessary files
    snakemake_files = ['snakemake/dentist.yml', 'snakemake/Snakefile', 'snakemake/snakemake.yml', 'snakemake/envs',
                       'snakemake/scripts']
    for file in snakemake_files:
        src = os.path.join(dentist_dir, file)
        subprocess.run(['cp', '-r', '-t', workdir, src], check=True)
    print("Snakemake workflow setup complete.")


def run_snakemake(workdir, use_conda=True, cores='1'):
    # Activate virtual environment if required
    # os.environ['PATH'] = f"{workdir}/bin:{os.environ['PATH']}"

    # Construct the snakemake command
    snakemake_cmd = ['snakemake', '--configfile=snakemake.yml', f'--cores={cores}']
    if use_conda:
        snakemake_cmd.append('--use-conda')
    else:
        snakemake_cmd.append('--use-singularity')

    # Run snakemake command
    subprocess.run(snakemake_cmd, cwd=workdir, check=True)
    print("Dentist workflow executed.")
