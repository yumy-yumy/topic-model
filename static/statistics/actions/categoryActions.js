import { SET_CATEGORY, LOAD_CATEGORIES } from '../constants/categoryConstants';
import AppDispatcher from '../dispatcher/appDispatcher';

const CategoryActions = {
  setCategory(newCategory){
    AppDispatcher.dispatch({
      actionType: SET_CATEGORY,
      newCategory: newCategory
    });
  },

  loadCategories(){
    AppDispatcher.dispatch({
      actionType: LOAD_CATEGORIES
    });
  }
}

export default CategoryActions;
