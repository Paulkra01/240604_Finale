import streamlit as st

def add_device_detection():
    # JavaScript zur Geräteerkennung und Hinzufügen eines "Back to Top" Buttons
    device_detection_js = """
    <script>
    function detectDevice() {
        var width = window.innerWidth;
        var deviceType = '';
        if (width <= 480) {
            deviceType = 'smartphone';
        } else if (width <= 768) {
            deviceType = 'tablet';
        } else {
            deviceType = 'laptop';
        }
        // Resultat an Streamlit senden
        window.parent.postMessage({deviceType: deviceType, width: width}, "*");

        // Back to Top Button
        var button = document.createElement('button');
        button.textContent = 'Back to Top';
        button.style.position = 'fixed';
        button.style.bottom = '10px';
        button.style.right = '10px';
        button.style.display = 'none';
        button.style.zIndex = '1000';
        button.onclick = function() {
            window.scrollTo({top: 0, behavior: 'smooth'});
        };
        document.body.appendChild(button);

        window.onscroll = function() {
            if (document.documentElement.scrollTop > 20) {
                button.style.display = 'block';
            } else {
                button.style.display = 'none';
            }
        };
    }
    window.onload = detectDevice;
    </script>
    """
    # Einbetten des JavaScript in Streamlit
    st.components.v1.html(device_detection_js)
