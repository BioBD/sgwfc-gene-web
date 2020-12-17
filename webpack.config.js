var path = require('path')
var webpack = require('webpack')
var BundleTracker = require('webpack-bundle-tracker')

module.exports = {
  entry:  path.join(__dirname, 'assets/src/js/index'),
  output: {
    path: path.resolve('assets/dist/'),
    publicPath: '/static/dist/',
    filename: "[name]-[hash].js",
  },
  optimization: {
    minimize: false
  },
  plugins: [
    new BundleTracker({
      path: __dirname,
      filename: 'webpack-stats.json'
    }),
  ],
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['es2015', 'react']
          }
        }
      },
      {
        test: /\.(?:le|c)ss$/,
        use: [
          require.resolve('style-loader'),
          {
            loader: require.resolve('css-loader'),
            options: {
              importLoaders: 1,
            },
          },
          {
            loader: require.resolve('less-loader'),
            options: {
              importLoaders: 1,
            },
          }
        ]
      }
    ],
  },
}