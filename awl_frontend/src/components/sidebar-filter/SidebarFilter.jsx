import React, { useState } from "react";
import "./sidebarfilter.css";
import {useFormContext} from "react-hook-form";

export default function SidebarFilter({filter_title, form_key, options}) {
    const { register, getValues} = useFormContext();
    const [showMore, setShowMore] = useState(false);
    const showButton = options.length > 5;
    const form_values = getValues(form_key)
    const selected_options = options.filter((e) => form_values?.includes(e.id))

    options = options.filter((e) => !selected_options.includes(e))
    options = !showMore ? options.slice(0, 4) : options
    return (
        <div className="sidebar-filter">
            <span className="filter-title">{filter_title}</span>
            {selected_options.map((option) =>
                <div key={`filter-form-input-container_${option.id}`} className="filter-form-input-container">
                    <label
                        title={option.name}
                        key={`filter-form-input-label_${option.id}`}
                        className="filter-form-input-label"
                    >
                        <input {...register(form_key)}
                               key={`filter-form-input_${option.id}`}
                               className="filter-form-input"
                               name={form_key}
                               type="checkbox"
                               value={option.id}
                        />
                        {option.name}
                    </label>
                </div>
            )}
            {options.map((option) =>
                <div key={`filter-form-input-container_${option.id}`} className="filter-form-input-container">
                    <label
                        title={option.name}
                        key={`filter-form-input-label_${option.id}`}
                        className="filter-form-input-label"
                    >
                        <input {...register(form_key)}
                            key={`filter-form-input_${option.id}`}
                            className="filter-form-input"
                            name={form_key}
                            type="checkbox"
                            value={option.id}
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
