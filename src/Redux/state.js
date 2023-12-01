const GET_floor = "GET_floor";
const GET_buildingname = "GET_buildingname";
const GET_data = "GET_data";
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
const init = {
  floor: null,
  buildingname: "",
  data: [],
};
export default function getelements(state = init, action) {
  switch (action.type) {
    case GET_buildingname:
      return { ...state, buildingname: action.buildingname };
    case GET_floor:
      return { ...state, floor: action.floor };
    case GET_data:
      return { ...state, data: action.data };
    default:
      return state;
  }
}
