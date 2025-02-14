// import React from "react";


// Card component (main card container)
export const Card = ({ children }) => {
  return (
    <div className="border rounded-lg p-4 shadow-lg bg-white">
      {children} {/* Render any children passed to the Card */}
    </div>
  );
};

// CardContent component (for inner content of the card)
export const CardContent = ({ children }) => {
  return <div className="flex flex-col items-start">{children}</div>;
};

