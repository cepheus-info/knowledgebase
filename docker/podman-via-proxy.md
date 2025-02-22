
# Guide to Configure V2Ray and Run Podman Compose on Windows with WSL

## Prerequisites

1. **Windows Subsystem for Linux (WSL)**: Ensure you have WSL installed (preferably WSL 2).
2. **Podman Installed**: Use the official Windows installer for Podman.
3. **Podman Compose Installed**: Install `podman-compose` using pip in your WSL environment:

   ```bash
   pip install podman-compose
   ```
4. **V2Ray Installed**: Ensure V2Ray is installed and configured properly on your Windows host.

## Step 1: Configure V2Ray to Listen on Local LAN IP

1. **Open the V2Ray Configuration File**:
   Locate your V2Ray configuration file, usually named `config.json`. This file is typically found in the V2Ray installation directory on Windows.

2. **Edit the `inbounds` Section**:
   Modify the `inbounds` section to ensure it listens on your local LAN IP address and is set up for HTTP traffic with sniffing enabled. Replace `10.39.1.41` with your actual LAN IP address.

   Example configuration:

   ```json
   {
     "inbounds": [
       {
         "port": 1080,
         "listen": "10.39.1.41",  // Your local LAN IP
         "protocol": "http",  // Using HTTP protocol
         "sniffing": {
           "enabled": true,
           "destOverride": [
             "http",
             "tls"
           ]
         },
         "settings": {
           "auth": "noauth",  // No authentication required
           "udp": true
         }
       }
     ],
     "outbounds": [
       {
         "protocol": "vmess",
         "settings": {
           // your outbound settings...
         }
       }
     ]
   }
   ```

   Save the changes and restart the V2Ray service.

## Step 2: Configure Proxy Settings for Podman

### 2.1 Set Environment Variables in Podman Configuration

#### Accessing the `containers.conf` File

You can access the `/etc/containers/containers.conf` file in two ways:

1. **Using Windows Explorer**:
   - Open **Windows Explorer** and navigate to **Linux** -> **podman-machine-default**.
   - Locate `containers.conf`.
   - Before editing, you may need to change the file's permissions using WSL.

2. **Using WSL Command**:
   - Open a command prompt and run:

     ```powershell
     wsl -d podman-machine-default
     ```

   - Then, you can edit the file using a text editor (e.g., `nano` or `vim`).

#### Editing the File

1. **Open the Podman Configuration File**:

   If you're using WSL, run:

   ```bash
   sudo nano /etc/containers/containers.conf
   ```

2. **Adjust Permissions (if using Windows Explorer)**:

   If you accessed the file via Windows Explorer, you might need to adjust permissions before editing. In WSL, run:

   ```bash
   sudo chmod 644 /etc/containers/containers.conf
   ```

3. **Add Proxy Settings**:
   Under the `[engine]` section, add the following lines, replacing `10.39.1.41` with your actual Windows host LAN IP:

   ```toml
   [engine]
   env = [
       "HTTP_PROXY=http://10.39.1.41:1080",
       "HTTPS_PROXY=http://10.39.1.41:1080",
       "NO_PROXY=localhost,127.0.0.1,::1"
   ]
   ```

4. **Save and Exit**: Save your changes and exit the editor (in nano, press `CTRL + X`, then `Y`, and `Enter`).

### 2.2 Restart Podman Service

You can restart the Podman machine using PowerShell:

1. **Stop the Podman Machine**:

   Open **PowerShell** and run:

   ```powershell
   podman machine stop
   ```

2. **Start the Podman Machine**:

   Run the following command to start Podman again:

   ```powershell
   podman machine start
   ```

Alternatively, you can restart the Podman service directly in WSL:

```bash
sudo systemctl restart podman
```

## Step 3: Create Your Podman Compose File

1. **Create a Directory for Your Project**:

   ```bash
   mkdir ~/my_podman_project
   cd ~/my_podman_project
   ```

2. **Create a `docker-compose.yml` File**:

   Create a `docker-compose.yml` file in your project directory:

   ```bash
   nano docker-compose.yml
   ```

   Example configuration for a simple web application using Nginx:

   ```yaml
   version: '3.8'
   services:
     webapp:
       image: nginx:latest
       ports:
         - "80:80"
       environment:
         - HTTP_PROXY=http://10.39.1.41:1080
         - HTTPS_PROXY=http://10.39.1.41:1080
         - NO_PROXY=localhost,127.0.0.1,::1
   ```

   Save and exit the editor.

## Step 4: Run Podman Compose

1. **Navigate to Your Project Directory**:

   ```bash
   cd ~/my_podman_project
   ```

2. **Run Podman Compose**:

   Use the following command to start your application:

   ```bash
   podman-compose up
   ```

   This command will download the necessary images and start the containers as defined in your `docker-compose.yml`.

## Step 5: Verify the Setup

1. **Check Running Containers**:

   After running `podman-compose up`, you can check the status of your containers with:

   ```bash
   podman ps
   ```

2. **Access Your Application**:

   Open a web browser and navigate to `http://localhost` or `http://<your_windows_host_ip>` to verify that your application is running and accessible.

## Additional Considerations

1. **Firewall Settings**: Ensure that your Windows firewall allows traffic on the ports you are using (e.g., port 80).

2. **Security**: Be cautious with proxy settings and access controls, especially if your V2Ray service is accessible over the LAN.

3. **Persistent Proxy Configuration**: If you want your proxy settings to be available in all terminal sessions, you can also add the proxy export commands to your `~/.bashrc` file in WSL:

   ```bash
   echo 'export HTTP_PROXY="http://10.39.1.41:1080"' >> ~/.bashrc
   echo 'export HTTPS_PROXY="http://10.39.1.41:1080"' >> ~/.bashrc
   echo 'export NO_PROXY="localhost,127.0.0.1,::1"' >> ~/.bashrc
   ```

   After adding, run `source ~/.bashrc` to apply the changes.

## Conclusion

By following this guide, you can successfully configure V2Ray to listen on your local LAN IP and run `podman-compose` on your Windows PC with WSL, utilizing the configured proxy settings. This setup allows your containers to access the internet through the proxy running on your Windows host while ensuring seamless integration between V2Ray, Podman, and WSL.

Feel free to modify the configurations as needed for your specific use case! If you have any further questions or need assistance, don't hesitate to ask.
