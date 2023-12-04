import React, { useState, useEffect, useRef, useCallback } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";
import axios from "axios";
import styled from "styled-components";
import EditCaption from "./EditCaption";
import Editupdown from "./Editupdown";
import { useSelector, useDispatch } from "react-redux";
import {
  getfloor,
  getbuildingname,
  getdata,
  getnewdata,
  getdfloor,
  getufloor,
} from "../Redux/state";

export default function Login() {
  const [Loading, setLoading] = useState(false);
  const [Buildingnames, setBuildingnames] = useState([]);
  const [Floors, setFloors] = useState([]);
  const [filteredOptionsB, setFilteredOptionsB] = useState([]);
  const [filteredOptionsF, setFilteredOptionsF] = useState([]);
  const [isDropdownOpenB, setIsDropdownOpenB] = useState(false);
  const [isDropdownOpenF, setIsDropdownOpenF] = useState(false);
  const newData = useSelector((state) => state.state.newdata);
  const Floor = useSelector((state) => state.state.floor);
  const api = useSelector((state) => state.state.url);
  const Buildingname = useSelector((state) => state.state.buildingname);
  const ref = useRef(null);

  const navigate = useNavigate();
  const dispatch = useDispatch();
  var url = `${api}/json/${Buildingname}_${Floor}`;
  var buildingsApi = `${api}/buildinglist`;
  var floorsApi = `${api}/dir/${Buildingname}`;
  var updateJson = `${api}/editstore/${Buildingname}_${Floor}`;

  const getBuildingnames = useCallback(async () => {
    await axios.get(buildingsApi).then((response) => {
      setBuildingnames(response.data);
    });
  }, [buildingsApi]);

  useEffect(() => {
    getBuildingnames();
  }, [getBuildingnames]);

  const findFloors = useCallback(async () => {
    try {
      setLoading(true);
      await axios.get(floorsApi).then((response) => {
        setFloors(response.data);
      });
    } catch (err) {
      console.log("에러 내역", err);
      setFloors(["404 err"]);
    }
    setLoading(false);
  }, [floorsApi]);

  useEffect(() => {
    findFloors();
  }, [Buildingname, findFloors]);

  const getstore = useCallback(async () => {
    try {
      setLoading(true);
      await axios.get(url).then((response) => {
        dispatch(getdata(response.data));
        dispatch(getnewdata(response.data));
        // console.log(response.data)
      });
    } catch (err) {
      console.log("에러 내역", err);
      dispatch(getdata([{ id: 404, caption: "404 Error" }]));
    }
    setLoading(false);
  }, [url, dispatch]);

  useEffect(() => {
    getstore();
    var Floor_;
    if (Floor[0] === "B") {
      Floor_ = -parseInt(Floor[1]);
    } else {
      Floor_ = parseInt(Floor);
    }
    // console.log(Floor_);
    var n_floor, p_floor;
    if (Floor_ === 1) {
      n_floor = 2;
      p_floor = -1;
    } else if (Floor_ === -1) {
      n_floor = 1;
      p_floor = -2;
    } else {
      n_floor = Floor_ + 1;
      p_floor = Floor_ - 1;
    }
    // console.log(n_floor, p_floor);
    dispatch(getufloor(n_floor.toString().padStart(2, "0").replace("-", "B")));
    dispatch(getdfloor(p_floor.toString().padStart(2, "0").replace("-", "B")));
  }, [Floor, dispatch, getstore]);

  const handleInputChangeB = (event) => {
    filterOptionsB(event.target.value);
  };

  const handleClickB = () => {
    setIsDropdownOpenB(true);
    filterOptionsB("");
  };
  const handleInputChangeF = (event) => {
    filterOptionsF(event.target.value);
  };

  const handleClickF = () => {
    setIsDropdownOpenF(true);
    filterOptionsF("");
  };
  const handleOptionClickBuilding = (option) => {
    dispatch(getbuildingname(option));
    setIsDropdownOpenB(false);
  };
  const handleOptionClickFloor = (option) => {
    dispatch(getfloor(option));
    setIsDropdownOpenB(false);
  };
  const filterOptionsB = (input) => {
    const filtered = Buildingnames.filter((option) =>
      option.toLowerCase().includes(input.toLowerCase())
    ).sort();
    setFilteredOptionsB(filtered);
  };
  const filterOptionsF = (input) => {
    const filtered = Floors.filter((option) =>
      option.toLowerCase().includes(input.toLowerCase())
    ).sort();
    setFilteredOptionsF(filtered);
  };
  useEffect(() => {
    function handleClickOutside(event) {
      if (ref.current && !ref.current.contains(event.target)) {
        setIsDropdownOpenB(false);
        setIsDropdownOpenF(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);
  const buttonClick = async () => {
    try {
      setLoading(true);
      console.log(newData);
      await axios.post(updateJson, { newData }).then((response) => {
        console.log(response.data);
      });
    } catch (err) {
      console.log("에러 내역", err);
    }
    setLoading(false);
  };
  const toUpdown = () => {
    getstore();
    navigate(`/editupdown`);
  };
  const toCaption = () => {
    getstore();
    navigate(`/`);
  };
  return (
    <div>
      <Forms ref={ref}>
        <Formtext>건물명: </Formtext>
        <Form>
          <Inputform
            type="text"
            value={Buildingname || ""}
            onChange={handleInputChangeB}
            onClick={handleClickB}
            placeholder="건물명을 검색하세요"
          />
          {isDropdownOpenB && (
            <Dropdownlist>
              {filteredOptionsB.map((option, index) => (
                <Dropdownli
                  key={index}
                  onClick={() => {
                    handleOptionClickBuilding(option);
                    setIsDropdownOpenB(false);
                  }}
                >
                  {option}
                </Dropdownli>
              ))}
            </Dropdownlist>
          )}
        </Form>
        <Formtext>층: </Formtext>
        <Form>
          <Inputform
            type="text"
            value={Floor || ""}
            onChange={handleInputChangeF}
            onClick={handleClickF}
            placeholder="층을 선택하세요"
          />
          {isDropdownOpenF && (
            <Dropdownlist>
              {filteredOptionsF.map((option, index) => (
                <Dropdownli
                  key={index}
                  onClick={() => {
                    handleOptionClickFloor(option);
                    setIsDropdownOpenF(false);
                  }}
                >
                  {option}
                </Dropdownli>
              ))}
            </Dropdownlist>
          )}
        </Form>
        <Routbutton onClick={toCaption}>
          {Loading ? "Loading" : "캡션 채우기"}
        </Routbutton>
        <Routbutton onClick={toUpdown}>
          {Loading ? "Loading" : "엘리베이터,\n 계단 연결"}
        </Routbutton>
        <Button onClick={buttonClick}>
          {Loading ? "Loading" : "변경사항 적용"}
        </Button>
      </Forms>
      <Routes>
        <Route path="/*" element={<EditCaption />} />
        <Route path="/editupdown" element={<Editupdown />} />
      </Routes>
    </div>
  );
}
const Forms = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
`;
const Formtext = styled.div`
  font-size: 20px;
  margin-right: 5px;
`;
const Form = styled.form`
  position: relative;
  width: 350px;
  height: 100px;
  display: flex;
  align-items: center;
`;
const Inputform = styled.input`
  padding-left: 20px;
  font-size: 15px;
  width: 200px;
  height: 40px;
  border-radius: 10px;
`;
const Button = styled.button`
  width: 160px;
  height: 50px;
  border-radius: 30px;
  font-size: 18px;
  background-color: #4677fc;
  color: white;
  cursor: pointer;
`;
const Routbutton = styled.button`
  width: 70px;
  height: 35px;
  border-radius: 10px;
  margin-right: 20px;
  font-size: 10px;
  background-color: rgb(105, 64, 255);
  color: white;
  cursor: pointer;
`;
const Dropdownlist = styled.ul`
  position: absolute;
  z-index: 1000;
  top: 60px;
  left: 10px;
  width: 200px;
  max-height: 200px;
  overflow-y: auto;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 10%;
  border-top: none;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  padding: 0;
  list-style: none;
`;
const Dropdownli = styled.li`
  padding: 10px;
  cursor: pointer;
  &:hover {
    background-color: #f1f1f1;
  }
`;
