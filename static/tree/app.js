(function(){
  'use strict'

  angular.module('treeApp', ['ngAnimate'])
    .config(function($interpolateProvider) {
      $interpolateProvider.startSymbol('{[');
      $interpolateProvider.endSymbol(']}');
    });
})();
