"""Post-processes pygbag's generated ``build/web/index.html`` to replace the
generic grey/green WebAssembly loader with a custom-branded Base Fibonacci
Division loading screen (animated Fibonacci tiles, golden spiral SVG, smooth
gradient progress bar, and fade-out transition into the game canvas).
"""
import sys
from pathlib import Path

CUSTOM_LOADER_SNIPPET = """
<!-- Base Fibonacci Division Custom Loader -->
<style id="fib-loader-style">
  html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 50% 28%, #232a48 0%, #161a2c 62%, #0e111f 100%) !important;
    color: #ecf0ff;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Inter, sans-serif;
    overflow: hidden;
  }
  canvas.emscripten {
    border: 0 !important;
    border-radius: 16px;
    box-shadow: 0 22px 60px rgba(0, 0, 0, 0.55), 0 0 0 1px rgba(126, 158, 255, 0.16);
  }
  /* Hide pygbag's default raw transfer UI while keeping its DOM nodes alive for scripts */
  #transfer, #status, #box, #dlg {
    opacity: 0 !important;
    pointer-events: none !important;
  }
  #fib-loader {
    position: fixed;
    inset: 0;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: radial-gradient(circle at 50% 30%, #242b4a 0%, #161a2c 64%, #0d101d 100%);
    transition: opacity 0.55s cubic-bezier(0.22, 1, 0.36, 1), transform 0.55s cubic-bezier(0.22, 1, 0.36, 1);
  }
  #fib-loader.fib-hidden {
    opacity: 0;
    transform: scale(1.03);
    pointer-events: none;
  }
  .fib-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 42px 52px 38px;
    border-radius: 24px;
    background: rgba(32, 38, 62, 0.86);
    border: 1px solid rgba(126, 158, 255, 0.22);
    box-shadow: 0 24px 64px rgba(0, 0, 0, 0.52), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    max-width: 480px;
    width: 88%;
    text-align: center;
  }
  .fib-ribbon {
    display: flex;
    gap: 10px;
    margin-bottom: 24px;
  }
  .fib-chip {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 15px;
    color: #ffffff;
    background: linear-gradient(180deg, #60a5fa 0%, #3878eb 100%);
    box-shadow: 0 6px 16px rgba(56, 120, 235, 0.38);
    animation: fibPulse 1.8s ease-in-out infinite;
  }
  .fib-chip.gold {
    background: linear-gradient(180deg, #facc15 0%, #eab308 100%);
    color: #161a2c;
    box-shadow: 0 6px 16px rgba(250, 204, 21, 0.35);
  }
  .fib-chip.mint {
    background: linear-gradient(180deg, #34d399 0%, #10a878 100%);
    box-shadow: 0 6px 16px rgba(52, 211, 153, 0.35);
  }
  @keyframes fibPulse {
    0%, 100% { transform: translateY(0) scale(1); filter: brightness(1); }
    50% { transform: translateY(-7px) scale(1.06); filter: brightness(1.12); }
  }
  .fib-title {
    font-size: 32px;
    font-weight: 800;
    letter-spacing: -0.02em;
    margin: 0 0 4px;
    color: #ecf0ff;
  }
  .fib-title span {
    color: #7e9eff;
  }
  .fib-subtitle {
    font-size: 14px;
    color: #96a2c8;
    margin: 0 0 26px;
  }
  .fib-bar-track {
    width: 100%;
    height: 10px;
    background: rgba(22, 26, 44, 0.85);
    border-radius: 999px;
    overflow: hidden;
    border: 1px solid rgba(126, 158, 255, 0.18);
    margin-bottom: 12px;
  }
  .fib-bar-fill {
    height: 100%;
    width: 12%;
    border-radius: 999px;
    background: linear-gradient(90deg, #60a5fa 0%, #7e9eff 50%, #34d399 100%);
    box-shadow: 0 0 14px rgba(126, 158, 255, 0.65);
    transition: width 0.2s ease-out;
  }
  .fib-status {
    font-size: 13px;
    font-weight: 600;
    color: #96a2c8;
    min-height: 18px;
  }
</style>

<div id="fib-loader" role="status" aria-live="polite">
  <div class="fib-card">
    <div class="fib-ribbon">
      <div class="fib-chip" style="animation-delay: 0.00s">21</div>
      <div class="fib-chip" style="animation-delay: 0.12s">13</div>
      <div class="fib-chip mint" style="animation-delay: 0.24s">8</div>
      <div class="fib-chip" style="animation-delay: 0.36s">5</div>
      <div class="fib-chip gold" style="animation-delay: 0.48s">3</div>
      <div class="fib-chip" style="animation-delay: 0.60s">2</div>
      <div class="fib-chip mint" style="animation-delay: 0.72s">1</div>
    </div>
    <h1 class="fib-title">Base Fibonacci <span>Division</span></h1>
    <p class="fib-subtitle">Factor numbers through Zeckendorf tile identities</p>
    <div class="fib-bar-track">
      <div id="fib-bar-fill" class="fib-bar-fill"></div>
    </div>
    <div id="fib-status-text" class="fib-status">Loading Python &amp; WebAssembly runtime…</div>
  </div>
</div>

<script>
(function() {
  var loader = document.getElementById("fib-loader");
  var fill = document.getElementById("fib-bar-fill");
  var statusText = document.getElementById("fib-status-text");
  var dismissed = false;

  window.dismissFibLoader = function() {
    if (dismissed || !loader) return;
    dismissed = true;
    if (fill) fill.style.width = "100%";
    if (statusText) statusText.textContent = "Ready!";
    loader.classList.add("fib-hidden");
    setTimeout(function() {
      if (loader && loader.parentNode) loader.parentNode.removeChild(loader);
    }, 650);
  };

  function syncProgress() {
    if (dismissed) return;
    var pg = document.getElementById("progress");
    var st = document.getElementById("status");
    var tr = document.getElementById("transfer");
    if (pg && pg.max && pg.value >= 0) {
      var pct = Math.max(10, Math.min(100, Math.round((pg.value / pg.max) * 100)));
      if (fill) fill.style.width = pct + "%";
    }
    if (st && st.textContent && st.textContent.trim()) {
      var txt = st.textContent.trim();
      if (statusText) statusText.textContent = txt;
      if (/hide|done|ready|running/i.test(txt)) {
        setTimeout(window.dismissFibLoader, 350);
        return;
      }
    }
    if (tr && (tr.style.display === "none" || tr.hidden)) {
      setTimeout(window.dismissFibLoader, 250);
      return;
    }
    requestAnimationFrame(syncProgress);
  }
  requestAnimationFrame(syncProgress);
  /* Fallback safety timeout so the overlay never blocks play if DOM IDs change */
  setTimeout(window.dismissFibLoader, 12000);
})();
</script>
"""


def patch_index_html(html: str) -> str:
    """Return patched HTML with dark theme colours and custom Fibonacci loader."""
    patched = html.replace("#7f7f7f", "#161a2c").replace("#808080", "#161a2c")
    if 'id="fib-loader"' in patched:
        return patched
    if "</body>" in patched:
        return patched.replace("</body>", CUSTOM_LOADER_SNIPPET + "\n</body>", 1)
    return patched + "\n" + CUSTOM_LOADER_SNIPPET


def patch_file(path) -> bool:
    target = Path(path)
    if not target.is_file():
        return False
    original = target.read_text(encoding="utf-8")
    updated = patch_index_html(original)
    target.write_text(updated, encoding="utf-8")
    return True


def main(argv=None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    target = Path(args[0]) if args else Path("build/web/index.html")
    if not patch_file(target):
        print(f"File not found: {target}", file=sys.stderr)
        return 1
    print(f"Patched web loading screen in {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
