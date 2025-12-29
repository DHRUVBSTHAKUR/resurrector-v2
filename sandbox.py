import docker
import os
import tarfile
import io

class Sandbox:
    def __init__(self, workspace_path="./agent_workspace"):
        self.client = docker.from_env()
        self.image = "python:3.12-alpine"
        self.workspace_path = os.path.abspath(workspace_path)
        
    def run_script(self, script_name="broken.py"):
        """
        Runs a script inside a secure Docker container.
        Returns: (exit_code, logs)
        """
        try:
            # 1. Prepare the build context (tar the workspace)
            # We tar the local workspace to send it into the container
            tar_stream = io.BytesIO()
            with tarfile.open(fileobj=tar_stream, mode='w') as tar:
                tar.add(self.workspace_path, arcname=".")
            tar_stream.seek(0)

            # 2. Start the container
            container = self.client.containers.run(
                self.image,
                command=f"python {script_name}",
                working_dir="/app",
                detach=True,
                tty=True,
                # We simply mount the volume for speed in V2
                volumes={self.workspace_path: {'bind': '/app', 'mode': 'rw'}} 
            )

            # 3. Wait for result
            result = container.wait()
            logs = container.logs().decode("utf-8")
            
            # 4. Cleanup
            container.remove()
            
            return result['StatusCode'], logs

        except Exception as e:
            return -1, f"🐳 Sandbox Error: {str(e)}"

# --- TEST BLOCK ---
if __name__ == "__main__":
    # Create a dummy file to test
    os.makedirs("./agent_workspace", exist_ok=True)
    with open("./agent_workspace/test.py", "w") as f:
        f.write("print('Hello from inside Docker!')")
    
    sb = Sandbox()
    code, output = sb.run_script("test.py")
    print(f"Exit Code: {code}")
    print(f"Output: {output}")