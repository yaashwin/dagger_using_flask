import dagger
import asyncio
import os

GIT_REPO = "https://github.com/yaashwin/jenkins_flask_project.git"
IMAGE_NAME = "flask_image_lts"
CONTAINER_NAME = "flask_container"
HOST_PORT = "8085"
CONTAINER_PORT = "5000"

async def main():
    async with dagger.Connection() as client:
        
        # Test Docker availability within Dagger by running 'docker ps' via exec
        test_docker = client.container().from_("docker:latest").with_exec(["docker", "ps"])
        result = await test_docker.stdout()
        print("Docker status from Dagger:", result)

        # Step 1: Clone the GitHub repository
        src = client.git(GIT_REPO).branch("main").tree()

        # Step 2: Build the Docker image
        image = (
            client.container()
            .from_("docker:latest")
            .with_mounted_directory("/app", src)
            .with_workdir("/app")
            .with_exec(["docker", "build", "-f", "/home/yaashwin/dagger_poc/dagger_flask_project/Dockerfile", "-t", IMAGE_NAME, "."])
        )

        # Step 3: Stop and remove existing container
        cleanup = client.container().from_("docker:latest").with_exec([
            "sh", "-c",
            f"docker ps -q -f name={CONTAINER_NAME} && docker stop {CONTAINER_NAME} && docker rm {CONTAINER_NAME} || true"
        ])

        # Step 4: Run the new container
        new_container = client.container().from_(IMAGE_NAME).with_exec([
            "docker", "run", "-d",
            "--name", CONTAINER_NAME,
            "-p", f"{HOST_PORT}:{CONTAINER_PORT}",
            IMAGE_NAME
        ])

        # Execute the pipeline
        await image.stdout()
        await cleanup.stdout()
        result = await new_container.stdout()

        print("Container started:", result)

if __name__ == "__main__":
    asyncio.run(main())
