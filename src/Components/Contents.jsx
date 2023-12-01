import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { useSelector, useDispatch } from "react-redux";
import { getdata } from "../Redux/state";

export default function Contents({ id, caption }) {
  const Data = useSelector((state) => state.state.data);
  const [newCaption, setnewCaption] = useState(caption);
  const [value, setnewvalue] = useState(caption);

  const dispatch = useDispatch();
  useEffect(() => {
    setnewvalue("");
  }, []);

  const updateItem = () => {
    const updatedItems = Data.map((item) => {
      if (item.id === id) {
        return { ...item, caption: newCaption };
      }
      return item;
    });
    dispatch(getdata(updatedItems));
  };
  const onSelectItem = (key) => {
    setnewCaption(key);
  };

  useEffect(() => {
    console.log(Data);
  }, [Data]);

  return (
    <Wrapper>
      <Info>
        <Namebox>{id}: </Namebox>
        <Date
          placeholder={caption}
          onfo
          onChange={(e) => {
            onSelectItem(e.target.value);
            setnewvalue(e.target.value);
            updateItem();
          }}
        />
      </Info>
    </Wrapper>
  );
}

const Wrapper = styled.span`
  position: relative;
  border-color: black solid 1px;
`;
const Info = styled.div`
  width: 150px;
  height: 30px;
  display: flex;
  justify-content: center;
`;
const Namebox = styled.div`
  font-size: 15px;
  padding-left: 20px;
  width: 50px;
  font-weight: bold;
  font-family: "굴림";
`;
const Date = styled.input`
  margin-left: 5px;
  width: 100px;
  font-size: 13px;
  border: solid, 1px;
`;
