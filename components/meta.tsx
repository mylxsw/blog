import React from 'react';

interface MetaProps {
  author: string;
  date: Date;
  tags?: string[];
}

const Meta: React.FC<MetaProps> = ({ author, date, tags }) => {
  const formattedDate = date.toLocaleDateString();

  return (
  <div className="nx-mb-8 nx-flex nx-gap-3">
    <div className="nx-grow dark:nx-text-gray-400 nx-text-gray-600">
      <div className="nx-not-prose nx-flex nx-flex-wrap nx-items-center nx-gap-1">
      {author}, {formattedDate} {tags && tags.map((tag, index) => (
        <span key={index} className="nx-ml-2 nx-text-sm nx-bg-gray-100 nx-py-0.5 nx-px-1 nx-rounded-md">{tag}</span>
      ))}
      </div>
    </div>
  </div>
  );
};

export default Meta;