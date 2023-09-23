import React, { useState } from "react";
import "./sidebarfilter.css";
import { useFormContext } from "react-hook-form"
import { HandleFormSubmit } from "../sidebar/Sidebar"

export default function SidebarFilter({filter_title, form_key, options}) {
    const { register, handleSubmit } = useFormContext()
    const [showMore, setShowMore] = useState(false);
    const showButton = options.length > 5;

    options = !showMore ? options.slice(0, 4) : options
    return (
        <div className="sidebar-filter">
            <span className="filter-title">{filter_title}</span>
            {options.map((option) =>
                <div key={`filter-form-input-container_${option.id}`} className="filter-form-input-container">
                    <label key={`filter-form-input-label_${option.id}`} className="filter-form-input-label">
                        <input {...register(form_key)}
                            key={`filter-form-input_${option.id}`}
                            className="filter-form-input"
                            name={form_key}
                            type="checkbox"
                            value={option.id}
                            onChange={handleSubmit(HandleFormSubmit)}
                        />
                        {option.name}
                    </label>
                </div>
            )}
            {showButton ?
                <div className={!showMore ? "show-more" : "show-less"} onClick={() => setShowMore(!showMore)} ></div>
                : null
            }
        </div>
    );
}
