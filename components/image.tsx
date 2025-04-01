import React from 'react';

interface ImageProps {
  src: string;
  maxWidth?: number | string;
}

const Image: React.FC<ImageProps> = ({ src, maxWidth }) => {
  return (
    <img 
      src={src}
      style={{ maxWidth: maxWidth || '100%' }}
      className="nx-rounded-lg nx-mx-auto mt-5 mb-5"
      alt=""
    />
  );
};

export default Image;
