package com.fibgame.android

import android.os.Bundle
import android.util.Log
import android.view.View
import android.webkit.ConsoleMessage
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebResourceError
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.enableEdgeToEdge
import androidx.activity.addCallback
import androidx.appcompat.app.AppCompatActivity
import java.io.InputStream

class MainActivity : AppCompatActivity() {

    companion object {
        private const val BASE_URL = "http://localhost/android_asset/"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        onBackPressedDispatcher.addCallback(this) { finish() }

        val webView = WebView(this)
        webView.setLayerType(View.LAYER_TYPE_HARDWARE, null)
        setContentView(webView)

        webView.settings.apply {
            javaScriptEnabled = true
            domStorageEnabled = true
            allowFileAccess = true
            allowContentAccess = true
            loadWithOverviewMode = true
            useWideViewPort = true
            builtInZoomControls = false
            displayZoomControls = false
            mediaPlaybackRequiresUserGesture = false
            mixedContentMode = android.webkit.WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
        }

        webView.webChromeClient = object : WebChromeClient() {
            override fun onConsoleMessage(msg: ConsoleMessage): Boolean {
                Log.d("WebView", "${msg.messageLevel()}: ${msg.message()} (${msg.sourceId()}:${msg.lineNumber()})")
                return true
            }
        }

        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                return false
            }

            override fun shouldInterceptRequest(view: WebView?, request: WebResourceRequest?): WebResourceResponse? {
                val urlStr = request?.url.toString()

                // Log CDN archive requests
                if (urlStr.contains("basefibonaccidivisiongame") || urlStr.contains("pygame-web")) {
                    Log.d("WebView", "CDN request: $urlStr")
                }

                // Intercept local asset requests
                val prefix = "http://localhost/android_asset/"
                if (urlStr.startsWith(prefix)) {
                    val assetPath = urlStr.removePrefix(prefix).split("?").first()
                    Log.d("WebView", "Intercept: $assetPath")
                    try {
                        val inputStream: InputStream = assets.open(assetPath)
                        val mimeType = when {
                            assetPath.endsWith(".tar.gz") -> "application/gzip"
                            assetPath.endsWith(".archive") -> "application/gzip"
                            assetPath.endsWith(".pygbag") -> "application/zip"
                            assetPath.endsWith(".png") -> "image/png"
                            assetPath.endsWith(".html") -> "text/html"
                            assetPath.endsWith(".js") -> "application/javascript"
                            assetPath.endsWith(".wasm") -> "application/wasm"
                            assetPath.endsWith(".data") -> "application/octet-stream"
                            assetPath.endsWith(".css") -> "text/css"
                            else -> "application/octet-stream"
                        }
                        return WebResourceResponse(mimeType, null, inputStream)
                    } catch (e: Exception) {
                        Log.e("WebView", "Asset not found: $assetPath")
                    }
                }

                // Intercept CDN archive requests - serve from local assets
                val cdnPrefix = "https://pygame-web.github.io/cdn/0.9.3/basefibonaccidivisiongame"
                if (urlStr.startsWith(cdnPrefix)) {
                    val fileNames = listOf("basefibonaccidivisiongame.archive", "basefibonaccidivisiongame.tar.gz", "basefibonaccidivisiongame.pygbag")
                    for (fileName in fileNames) {
                        try {
                            val inputStream: InputStream = assets.open(fileName)
                            Log.d("WebView", "Intercepting CDN archive: $fileName")
                            return WebResourceResponse("application/gzip", null, inputStream)
                        } catch (_: Exception) { }
                    }
                    Log.e("WebView", "Could not open archive from assets (tried $fileNames)")
                }

                return null
            }

            override fun onReceivedError(view: WebView?, request: WebResourceRequest?, error: WebResourceError?) {
                Log.e("WebView", "Error ${error?.errorCode} for ${request?.url}: ${error?.description}")
            }

            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
                Log.d("WebView", "Page finished: $url")
            }
        }

        webView.loadUrl("${BASE_URL}index.html")
    }
}
