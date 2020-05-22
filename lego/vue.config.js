module.exports = {
  publicPath: "/",
  devServer: {
    proxy: {
      "/api": {
        target: "https://localhost:8000/"
      }
    }
  },
  transpileDependencies: ["vuetify"]
};
