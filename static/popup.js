
        # COMING SOON POPUP
        <script type="text/javascript">
          document.addEventListener("DOMContentLoaded", function () {
            const popup = document.getElementById("popup");
            const popupText = document.getElementById("popup-text");
            const popupClose = document.getElementById("popup-close");
          };

          // Close on X
          popupClose.onclick = function () {
            popup.classList.add("popup-hidden");
          };

          // Close on outside click
          popup.onclick = function (e) {
            if (e.target === popup) {
              popup.classList.add("popup-hidden");
            }
          };

          // Make globally accessible
          window.showPopup = function (text) {
            popupText.textContent = text;
            popup.classList.remove("popup-hidden");
          };
  );
        </script>