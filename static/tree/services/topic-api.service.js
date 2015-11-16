(function(){
  'use strict';

  angular.module('treeApp')
    .factory('TopicApi', TopicApi);

  TopicApi.$inject = ['$http', '$q'];

  function TopicApi($http, $q){
    var service = {
      getTopics: getTopics
    }

    function getTopics(){
      var deferred = $q.defer();

      var topics = [];

      _.times(40, function(){
        topics.push({ title: 'Lorem ipsum dolor sit amet '});
      });

      topics.forEach(function(topic){
        topic.children = [];

        _.times(20, function(){
          topic.children.push({ title: 'Lorem ipsum dolor sit amet '});
        });

        topic.children.forEach(function(child){
          child.children = [];

          _.times(10, function(){
            child.children.push({ title: 'Lorem ipsum dolor sit amet '});
          });
        });
      });

      deferred.resolve(topics);

      return deferred.promise;
    }

    return service;
  }
})();
