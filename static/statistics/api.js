import $ from 'jquery';
import _ from 'lodash';

const Api = {
  getAllCategories(){
    return $.get('/class/arxiv-category');
  },
  getTopicsFromCategory(category){

    return $.get(`/statistics_for_class/${category.replace(/ /g, '+')}`)
    /*return {
      done: function(callback){
        var years = [];
        _.times(23, function(i){
          let year = { year: i + 1993 };
          year.topics = [];

          _.times(40, function(){
            let txt = 'Lorem ipsum dolor sit amet';
            year.topics.push({ title: txt.substring(_.random(0, txt.length / 2), _.random(txt.length/2, txt.length)), weight: Math.random() });
          });

          years.push(year);
        });

        callback(years);
      }
    }*/
  }
};

export default Api;
