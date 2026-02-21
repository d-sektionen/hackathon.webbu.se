export default (pollen) => ({
  output: "./app/pollen.css",
  module: {
    colors: {
      ...pollen,
      grey: "var(--color-gray-500)",
    },
  },
});
