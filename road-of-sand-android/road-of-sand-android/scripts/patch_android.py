"""Make the Android app borderless: hide the status and navigation bars
(immersive mode), draw under the camera notch, keep the screen awake,
and set the screen orientation. Run after `npx cap add android`."""
import os, re, sys

APP_ID = "com.bombinator.roadofsand"
ORIENTATION = os.environ.get("ORIENTATION", "sensorLandscape")  # or "unspecified" to allow portrait

pkg_dir = os.path.join("android", "app", "src", "main", "java", *APP_ID.split("."))
os.makedirs(pkg_dir, exist_ok=True)
with open(os.path.join(pkg_dir, "MainActivity.java"), "w") as f:
    f.write(f"""package {APP_ID};

import android.os.Build;
import android.os.Bundle;
import android.view.WindowManager;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {{
    @Override
    public void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        goBorderless();
    }}

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {{
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) goBorderless();
    }}

    private void goBorderless() {{
        WindowCompat.setDecorFitsSystemWindows(getWindow(), false);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {{
            WindowManager.LayoutParams lp = getWindow().getAttributes();
            lp.layoutInDisplayCutoutMode = WindowManager.LayoutParams.LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES;
            getWindow().setAttributes(lp);
        }}
        WindowInsetsControllerCompat c = WindowCompat.getInsetsController(getWindow(), getWindow().getDecorView());
        c.hide(WindowInsetsCompat.Type.systemBars());
        c.setSystemBarsBehavior(WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
    }}
}}
""")

manifest = os.path.join("android", "app", "src", "main", "AndroidManifest.xml")
xml = open(manifest).read()
xml = re.sub(r'\s*android:screenOrientation="[^"]*"', "", xml)
xml, n = re.subn(r"(<activity\b)", rf'\1 android:screenOrientation="{ORIENTATION}"', xml, count=1)
if n != 1:
    sys.exit("Could not find <activity> in AndroidManifest.xml")
open(manifest, "w").write(xml)
print(f"Borderless MainActivity written; orientation = {ORIENTATION}")
