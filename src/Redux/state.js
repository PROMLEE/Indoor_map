const GET_floor = "GET_floor";
const GET_dfloor = "GET_dfloor";
const GET_ufloor = "GET_ufloor";
const GET_buildingname = "GET_buildingname";
const GET_data = "GET_data";
const GET_newdata = "GET_newdata";
const UPDATE_DATA_ITEM = "UPDATE_DATA_ITEM";
const UPDATE_DATA_UPDOWN = "UPDATE_DATA_UPDOWN";

export const updateDataItem = (id, newCaption, newup, newdown) => {
  return {
    type: UPDATE_DATA_ITEM,
    payload: { id, newCaption, newup, newdown },
  };
};
// export const updateUpdown = (id, up, down) => {
//   return {
//     type: UPDATE_DATA_ITEM,
//     payload: { id, up, down },
//   };
// };
export const getfloor = (floor) => {
  return {
    type: GET_floor,
    floor,
  };
};
export const getufloor = (ufloor) => {
  return {
    type: GET_ufloor,
    ufloor,
  };
};
export const getdfloor = (dfloor) => {
  return {
    type: GET_dfloor,
    dfloor,
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
  floor: 1,
  buildingname: "",
  data: [{ id: 404, caption: "404 Error", move_up: 404, move_down: 404 }],
  newdata: [{ id: 404, caption: "404 Error", move_up: 404, move_down: 404 }],
  url: "http://127.0.0.1:8080",
  // url: "https://indoormap.store",
  ufloor: null,
  dfloor: null,
};
export default function getelements(state = init, action) {
  switch (action.type) {
    case GET_buildingname:
      return { ...state, buildingname: action.buildingname };
    case GET_floor:
      return { ...state, floor: action.floor };
    case GET_ufloor:
      return { ...state, ufloor: action.ufloor };
    case GET_dfloor:
      return { ...state, dfloor: action.dfloor };
    case GET_data:
      return { ...state, data: action.data };
    case GET_newdata:
      return { ...state, newdata: action.newdata };
    case UPDATE_DATA_ITEM:
      return {
        ...state,
        newdata: state.newdata.map((item) =>
          item.id === action.payload.id
            ? { ...item, caption: action.payload.newCaption, move_up: action.payload.newup,
              move_down: action.payload.newdown,}
            : item
        ),
      };
    // case UPDATE_DATA_UPDOWN:
    //   return {
    //     ...state,
    //     newdata: state.newdata.map((item) =>
    //       item.id === action.payload.id
    //         ? {
    //             ...item,
    //             move_up: action.payload.up,
    //             move_down: action.payload.payload.down,
    //           }
    //         : item
    //     ),
    //   };
    default:
      return state;
  }
}
