import React from "react";
import {
  faYoutube,
  faGithub,
  faFacebook,
} from "@fortawesome/free-brands-svg-icons";
import { faCopyright } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import './Footer.css'

export const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="item2">
          <span style={{ paddingRight: 5 }}>Copyright </span>
          <FontAwesomeIcon icon={faCopyright} />{" "}
          <span style={{ paddingLeft: 5 }}>
            {new Date().getFullYear()} YourCompany. All Rights
            Reserved.
          </span>
        </div>
        <a
          href="https://github.com/"
          target="_blank"
          className="item3"
          rel="noopener noreferrer"
        >
          <FontAwesomeIcon icon={faGithub} />
        </a>
        <a
          href="http://fb.com/"
          target="_blank"
          className="item4"
          rel="noopener noreferrer"
        >
          <FontAwesomeIcon icon={faFacebook} />
        </a>
        <a
          href="https://www.youtube.com/"
          target="_blank"
          className="item5"
          rel="noopener noreferrer"
        >
          <FontAwesomeIcon icon={faYoutube} />
        </a>

      </div>
    </footer>
  );
};