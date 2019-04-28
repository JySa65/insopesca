const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");

const miniCssExtractPlugin = new MiniCssExtractPlugin({
	filename: 'main.css',
	chunkFilename: '[id].css'
})

const optimizeCSSAssetsPlugin = new OptimizeCSSAssetsPlugin({})

module.exports = {
	mode: "production",
	entry: './src/index.js',
	output: {
		filename: 'main.js',
		path: path.resolve(__dirname, 'static')
	},
	module: {
		rules: [
			{
				test: /\.js$/,
				exclude: /node_modules/,
				loader: "babel-loader"
			},
			{
				test: /\.(css|scss)$/,
				use: [
					MiniCssExtractPlugin.loader,
					'css-loader',
					'sass-loader'
				]
			},
			{
				test: /\.(png|jpg|jpeg)$/,
				use: [
					'file-loader'
				]
			}
		]
	},
	plugins: [
		miniCssExtractPlugin,
		optimizeCSSAssetsPlugin,
	]
};

// const path = require('path');

// module.exports = {
// 	mode: "development",
// 	entry: path.resolve(__dirname, 'src', 'index.js'),
// 	output: {
// 		filename: 'main.js',
// 		path: path.resolve(__dirname, 'public', 'js')
// 	},
// 	module: {
// 		rules: [
// 			{
// 				test: /\.js$/,
// 				exclude: /node_modules/,
// 				loader: "babel-loader"
// 			},
// 			{
// 				test: /\.(css|scss)$/,
// 				use: [
// 					'style-loader',
// 					'css-loader',
// 					'sass-loader'
// 				]
// 			}
// 		]
// 	},
	// target: "node",
	// node: {
	// 	__dirname: true,
	// 	__filename: true,
	// },
	// externals: {
	// 	uws: "uws"
	// },
// };
