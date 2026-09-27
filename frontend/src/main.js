import { createApp } from 'vue';
import ElementPlus from 'element-plus';
import zhCn from 'element-plus/es/locale/lang/zh-cn';
import 'element-plus/dist/index.css';
import './styles.css';
import App from './App.vue';

const app = createApp(App);
app.use(ElementPlus, { locale: zhCn });
app.config.errorHandler = (err, inst, info) => {
  console.error('VUE-ERR:', info, '|', err.message, '| comp:', inst && inst.type && (inst.type.__name || inst.type.name), '\n', err && err.stack);
};
app.mount('#app');
