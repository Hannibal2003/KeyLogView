# Inputs To Mail.
Get Keyboard,Mouse,ScreenShot,Microphone Inputs and Send to your Mail.
Purpose of the project is testing the security of information systems

## USAGE

•**Set your Gmail address and app password in `keylogger.py`.**
•**Ensure you have enabled 'less secure app access' or generated an app password for your Gmail account.**


•**pip install -r requirements.txt**

•**python3 keylogger.py**

*Note: The README mentions a self-deletion feature if the code is discovered, but this functionality is not implemented in the current version.*

•
## Secure Credential Management

To enhance security, email credentials are now read from environment variables: `EMAIL_USER` and `EMAIL_PASS`.

**Setting Environment Variables:**

*   **Windows (Command Prompt):**
    ```bash
    set EMAIL_USER=your_email@gmail.com
    set EMAIL_PASS=your_app_password
    ```
    *Note: These variables are set for the current session only. For persistent storage, consider using system environment variable settings.*

*   **Windows (PowerShell):**
    ```powershell
    $env:EMAIL_USER="your_email@gmail.com"
    $env:EMAIL_PASS="your_app_password"
    ```

*   **Linux/macOS (Bash/Zsh):**
    ```bash
    export EMAIL_USER="your_email@gmail.com"
    export EMAIL_PASS="your_app_password"
    ```
    *Note: Add these lines to your shell profile (e.g., `.bashrc`, `.zshrc`) for persistence.*

Please ensure you have generated an app password for your Gmail account if you are using 2-factor authentication.



