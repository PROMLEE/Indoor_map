import { combineReducers } from "redux";
import { configureStore } from "@reduxjs/toolkit";

import state from "./state";

const rootReducer = combineReducers({
  state,
});
const store = configureStore({ reducer: rootReducer });
export default store;
