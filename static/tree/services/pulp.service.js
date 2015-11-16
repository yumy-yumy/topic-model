(function(){
  'use strict';

  angular.module('treeApp')
    .factory('PulpService', PulpService);

  PulpService.$inject = ['$window'];

  function PulpService($window){
    var PULP_URL = 'http://localhost:8000';

    var service = {
      toPulp: toPulp
    }

    function toPulp(options){
      $window.open(PULP_URL + '/search#/?query=' + options.query, '_blank');
    }

    return service;
  }
})();
