import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { useDispatch } from "react-redux";
import { updateDataItem } from "../Redux/state";

export default function Contents({ id, caption }) {
  const backupcaption = caption;
  const [newCaption, setnewCaption] = useState();
  const [value, setnewvalue] = useState();

  const dispatch = useDispatch();
  useEffect(() => {
    setnewvalue(caption);
    setnewCaption();
  }, [caption]);

  const updateItem = () => {
    if (newCaption) dispatch(updateDataItem(id, newCaption));
    else dispatch(updateDataItem(id, backupcaption));
  };

  return (
    <Wrapper>
      <Info>
        <Namebox>{id}: </Namebox>
        <Date
          placeholder={value || ""}
          value={newCaption || ""}
          onChange={(e) => {
            setnewCaption(e.target.value);
          }}
          onBlur={updateItem}
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
  align-items: center;
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
