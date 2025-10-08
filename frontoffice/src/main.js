import "./assets/main.css";

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import axios from "axios";

axios.defaults.baseURL = "http://127.0.0.1:8000";

createApp(App).use(vuetify).use(router).mount("#app");
