import React, { forwardRef } from "react";
import PropTypes from "prop-types";

// eslint-disable-next-line react/display-name
const Page = forwardRef(({ children, ...rest }, ref) => {
  return (
    <div ref={ref} {...rest}>
      {children}
    </div>
  );
});

Page.propTypes = {
  children: PropTypes.node.isRequired
};

export default Page;
