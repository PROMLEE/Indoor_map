import React, { useState, useEffect, useRef, useCallback } from "react";
import axios from "axios";
import styled from "styled-components";
import Contents from "./Contents";
import { useSelector, useDispatch } from "react-redux";
import { getfloor, getbuildingname, getdata } from "../Redux/state";

export default function Login() {
  const [Loading, setLoading] = useState(false);
  const [Buildingnames, setBuildingnames] = useState([]);
  const [Floors, setFloors] = useState([]);
  const [filteredOptionsB, setFilteredOptionsB] = useState([]);
  const [filteredOptionsF, setFilteredOptionsF] = useState([]);
  const [isDropdownOpenB, setIsDropdownOpenB] = useState(false);
  const [isDropdownOpenF, setIsDropdownOpenF] = useState(false);

  const Data = useSelector((state) => state.state.data);
  const Floor = useSelector((state) => state.state.floor);
  const Buildingname = useSelector((state) => state.state.buildingname);
  const ref = useRef(null);

  const dispatch = useDispatch();
  var api = "http://127.0.0.1:5000/";
  var url = `${api}/json/${Buildingname}_${Floor}`;
  var buildingsApi = `${api}/buildinglist`;
  var floorsApi = `${api}/dir/${Buildingname}`;
  var maskImg = `${api}/mask/${Buildingname}_${Floor}`;
  var realImg = `${api}/source/${Buildingname}_${Floor}`;

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
      });
      // console.log(data);
    } catch (err) {
      console.log("에러 내역", err);
      dispatch(getdata([{ id: 404, caption: "404 Error" }]));
    }
    setLoading(false);
  }, [url, dispatch]);

  useEffect(() => {
    getstore();
  }, [Floor, getstore]);

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
    dispatch(getbuildingname(option)); // 선택된 옵션으로 입력값 변경
    setIsDropdownOpenB(false); // 드롭다운 닫기
  };
  const handleOptionClickFloor = (option) => {
    dispatch(getfloor(option)); // 선택된 옵션으로 입력값 변경
    setIsDropdownOpenB(false); // 드롭다운 닫기
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
  return (
    <div>
      <Forms ref={ref}>
        <Formtext>건물명: </Formtext>
        <Form>
          <Inputform
            type="text"
            value={Buildingname}
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
            value={Floor}
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
        <Button>{Loading ? "Loading" : "변경사항 적용"}</Button>
      </Forms>
      <Appform>
        {Data.map((item) => {
          return <Contents id={item.id} caption={item.caption} key={item.id} />;
        })}
      </Appform>
      <Images>
        <Maskimg src={maskImg} />
        <Maskimg src={realImg} />
      </Images>
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
const Appform = styled.div`
  background-color: #bbbbbb29;
  width: 60%;
  overflow: scroll;
  height: 200px;
  border-radius: 5%;
  margin: auto;
  display: flex;
  flex-wrap: wrap;
  padding: 20px;
  padding-left: 50px;
  gap: 20px;
  border: black;
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
const Images = styled.div`
  display: flex;
  margin-top: 40px;
  justify-content: center;
  align-items: center;
  gap: 10px;
`;
const Maskimg = styled.img`
  align-items: center;
  height: 800px;
  width: 800px;
`;
