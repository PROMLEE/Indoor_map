const GET_floor = "GET_floor";
const GET_buildingname = "GET_buildingname";
const GET_data = "GET_data";
const GET_newdata = "GET_newdata";
const UPDATE_DATA_ITEM = "UPDATE_DATA_ITEM";

export const updateDataItem = (id, newCaption) => {
  return {
    type: UPDATE_DATA_ITEM,
    payload: { id, newCaption },
  };
};

export const getfloor = (floor) => {
  return {
    type: GET_floor,
    floor,
  };
};
export const getbuildingname = (buildingname) => {
  return {
    type: GET_buildingname,
    buildingname,
  };
};
export const getdata = (data) => {
  return {
    type: GET_data,
    data,
  };
};
export const getnewdata = (newdata) => {
  return {
    type: GET_newdata,
    newdata,
  };
};
const init = {
  floor: null,
  buildingname: "",
  data: [],
  newdata: [],
};
export default function getelements(state = init, action) {
  switch (action.type) {
    case GET_buildingname:
      return { ...state, buildingname: action.buildingname };
    case GET_floor:
      return { ...state, floor: action.floor };
    case GET_data:
      return { ...state, data: action.data };
    case GET_newdata:
      return { ...state, newdata: action.newdata };
    case UPDATE_DATA_ITEM:
      return {
        ...state,
        newdata: state.newdata.map((item) =>
          item.id === action.payload.id
            ? { ...item, caption: action.payload.newCaption }
            : item
        ),
      };
    default:
      return state;
  }
}
