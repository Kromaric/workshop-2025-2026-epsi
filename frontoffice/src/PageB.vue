
<script>
export default {
  data() {
    return {
      button2Unlocked: false
    };
  },
  mounted() {
    this.checkStatus();
    this.interval = setInterval(this.checkStatus, 100); // vérifie toutes les 2 secondes
  },
  beforeUnmount() {
    clearInterval(this.interval);
  },
  methods: {

    async checkStatus() {
      const res = await fetch("http://localhost:8000/status");
      const data = await res.json();
      this.button2Unlocked = data.button_unlocked;
    }
  }
}
</script>



<template>
  <div>
    <h1>Page B</h1>
    <button :disabled="!button2Unlocked">Button2</button>
  </div>
</template>
