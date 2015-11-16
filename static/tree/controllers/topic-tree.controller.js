(function(){
  'use strict';

  angular.module('treeApp')
    .controller('TopicTreeController', TopicTreeController);

  TopicTreeController.$inject = ['TopicApi', 'PulpService'];

  function TopicTreeController(TopicApi, PulpService){
    var vm = this;

    var chosenTopicsCount = 0;
    var chosenTopics = [];

    vm.expanded = true;
    vm.topicDisplayLimit = 20;
    vm.toggleChooseTopic = toggleChooseTopic;
    vm.toggleActivateTopic = toggleActivateTopic;
    vm.toggleExpandTopic = toggleExpandTopic;
    vm.loadMoreTopics = loadMoreTopics;
    vm.startSearch = startSearch;

    TopicApi.getTopics()
      .then(function(topics){
        vm.topics = topics;
      });

    function toggleChooseTopic(topic) {
      topic.chosen = !topic.chosen;

      if (topic.chosen) {
        chosenTopicsCount++;
        chosenTopics.push(topic);
      } else {
        chosenTopicsCount--;
        removeFromChosenTopics(topic);
      }

      vm.topicIsChosen = ( chosenTopicsCount > 0 );
    }

    function toggleActivateTopic(topic) {
      if (!topic.activated) {
        vm.topics.forEach(function(topic) {
          topic.activated = false
        });
      }

      topic.activated = !topic.activated;

      if (topic.activated) {
        vm.activeTopic = topic;
        vm.expanded = false;
      } else {
        vm.expanded = true;
        vm.activeTopic = null;
      }
    }

    function loadMoreTopics() {
      vm.topicDisplayLimit += 20;
    }

    function toggleExpandTopic(topic) {
      topic.expanded = !topic.expanded;
    }

    function startSearch(){
      var chosenTopicsToStr = _.chain(chosenTopics).map(function(t) { return t.title }).uniq().join(' ').split(' ').uniq().value().join('+');

      PulpService.toPulp({ query: chosenTopicsToStr });
    }

    function removeFromChosenTopics(topic) {
      var removedIndex = 0;

      chosenTopics.forEach(function(t, index) {
        if (t.title == topic.title) {
          removedIndex = index;
        }
      });

      chosenTopics.splice(removedIndex, 1);
    }
  }
})();
