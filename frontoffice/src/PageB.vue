<script>
export default {
  data() {
    return {
      // Variable état initial
      button2Unlocked: false,
      socket: null
    };
  },
  mounted() {
    // Ouvre la WebSocket
    this.socket = new WebSocket("ws://localhost:8000/ws");

    this.socket.onmessage = (event) => {
      // Gestion des events
      if (event.data === "unlocked") {
        this.button2Unlocked = true;
      }
    };

    this.socket.onclose = () => {
      console.log("WebSocket fermé");

    };
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.close();
    }
  }
}
</script>


<!-- Accès Page B: /page-b : voir ./router/index.js  -->
<template>
  <div>
    <h1>Page B</h1>
    <button :disabled="!button2Unlocked">Button2</button>
  </div>
</template>
