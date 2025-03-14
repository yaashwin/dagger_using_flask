import dagger
import asyncio
import subprocess

async def main():
    async with dagger.Connection() as client:
        # Step 1: Define the Docker build context
        docker_context = client.host().directory("/home/yaashwin/dagger_poc/dagger_flask_project")

        # Step 2: Build the Docker Image
        image = client.container().build(context=docker_context, dockerfile="Dockerfile")

        # Step 3: Export the image as a tarball
        image_tar = "/home/yaashwin/dagger_flask_app.tar"
        await image.export(image_tar)
        print(f"✅ Image exported as {image_tar}")

        # Step 4: Load the image into Docker
        subprocess.run(["docker", "load", "-i", image_tar], check=True)
        print("✅ Image successfully loaded into Docker")

# Run the pipeline
asyncio.run(main())
