# Keep AndroidX WebKit
-keep class androidx.webkit.** { *; }

# WebView JavaScript interface
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}
