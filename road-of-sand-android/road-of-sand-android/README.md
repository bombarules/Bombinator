# Road of Sand for Android

1. Make a new GitHub repository and upload everything in this folder (keep the `.github` folder).
2. Open the **Actions** tab. The "Build Android APK" workflow runs on every push to `main`, or press **Run workflow**.
3. When it finishes (about 5 minutes), open the run and download **road-of-sand-apk** under Artifacts. Unzip it to get `app-debug.apk`.
4. Copy the APK to your phone and open it. Android will ask you to allow installs from that app the first time.

To update the game, replace `www/index.html` with a new copy and push.

Orientation: the app locks to landscape. To allow portrait too, run the workflow by hand and set orientation to `unspecified`.

Linking devices (phone controllers, crowd voting) only works when the game is opened in Claude. In the APK, use Bluetooth controllers or two players on one screen.
