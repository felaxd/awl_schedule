import React, { useState } from "react";
import "./sidebarfilter.css";

export default function SidebarFilter({filter_title, options}) {
    const [selectedOptions, setSelectedOptions] = useState([]);
    const [showMore, setShowMore] = useState(false);
    const showButton = options.length > 5;
    const handleOptionChange = (e) => {
        const optionId = e.target.value;
        if (selectedOptions.includes(optionId)) {
            setSelectedOptions(selectedOptions.filter((id) => id !== optionId));
        } else {
            setSelectedOptions([...selectedOptions, optionId]);
        }
    };

    options = !showMore ? options.slice(0, 4) : options
    return (
        <div className="sidebar-filter">
            <span className="filter-title">{filter_title}</span>
            <form>
                {options.map((option) =>
                    <div>
                        <label>
                            <input
                                type="checkbox"
                                value={option.id}
                                onChange={handleOptionChange}
                                checked={selectedOptions.includes(option.id)}
                            />
                            {option.name}
                        </label>
                    </div>
                )}
            </form>
            {showButton ?
                <div className={!showMore ? "show-more" : "show-less"} onClick={() => setShowMore(!showMore)} ></div>
                : null
            }
        </div>
    );
}
