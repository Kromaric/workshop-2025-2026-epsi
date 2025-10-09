<script>
export default {
  methods: {
    async unlockButton2() {
      await fetch("http://localhost:8000/unlock", { method: "POST" });
    }
  }
}
</script>

<!-- Accès Page A: / : voir ./router/index.js  -->
<template>
  <div>
    <h1>Page A</h1>
    <button @click="unlockButton2">Débloquer Button2</button>
  </div>
</template>
