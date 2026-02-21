import { defineConfig, presetIcons, transformerDirectives } from "unocss";

export default defineConfig({
  presets: [presetIcons()],
  transformers: [transformerDirectives()],
});
