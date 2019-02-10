const path = require('path');

module.exports = {
	mode: "development",
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
					'style-loader',
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
	}
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
