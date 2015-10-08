import AppDispatcher from '../dispatcher/appDispatcher';
import Api from '../api';
import { EventEmitter } from 'events';
import { SET_CATEGORY, LOAD_CATEGORIES } from '../constants/categoryConstants';

const CHANGE_EVENT = 'CHANGE_EVENT';

var storeData = {
  categories: [],
  chosenCategory: '',
  years: [],
  loadingTopics: false
}

function chooseCategory(category){
  storeData.chosenCategory = category;
}

function setLoading(status){
  storeData.loadingTopics = status;
}

function setYears(years){
  storeData.years = years;
}

function setCategories(categories){
  storeData.categories = categories;
}

const CategoryStore = Object.assign({}, EventEmitter.prototype, {
  getAll(){
    return storeData;
  },

  emitChange() {
    this.emit(CHANGE_EVENT);
  },

  addChangeListener(callback){
    this.on(CHANGE_EVENT, callback);
  },

  removeChangeListener(callback) {
    this.removeListener(CHANGE_EVENT, callback);
  }
});

AppDispatcher.register((action) => {
  switch(action.actionType){
    case SET_CATEGORY:
      chooseCategory(action.newCategory);

      setLoading(true);
      CategoryStore.emitChange();

      Api.getTopicsFromCategory(action.newCategory)
        .done((data) => {
          setYears(JSON.parse(data));
          setLoading(false);
          CategoryStore.emitChange();
        });

      break;

    case LOAD_CATEGORIES:
      Api.getAllCategories()
        .done((data) => {
          setCategories(JSON.parse(data).classes);
          CategoryStore.emitChange();
        });

      break;

    default:
      // nop
  }
});

export default CategoryStore;
