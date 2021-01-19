pragma solidity 0.4.25;
pragma experimental ABIEncoderV2;

contract Stat {
    struct record {
        string[] hr;
        string[] bp;
        string[] temp;
        string[] gl;
        string[] ox;
        string[] res;
        string[] steps;
        string[] create;
    }
    
    mapping(string=>record)r_data;
    
    function addRecord(string hr_value, string bp_value, string temp_value, string gl_value, string ox_value, string res_value, string steps_value, string create_value, string emp_id) public {
        r_data[emp_id].hr.push(hr_value);
        r_data[emp_id].bp.push(bp_value);
        r_data[emp_id].temp.push(temp_value);
        r_data[emp_id].gl.push(gl_value);
        r_data[emp_id].ox.push(ox_value);
        r_data[emp_id].res.push(res_value);
        r_data[emp_id].steps.push(steps_value);
        r_data[emp_id].create.push(create_value);
    }
    
    function readRecord(string emp_id) public view returns(string[], string[], string[], string[], string[], string[]) {
        return (r_data[emp_id].hr, 
        r_data[emp_id].bp
        ,r_data[emp_id].temp
        ,r_data[emp_id].gl
        ,r_data[emp_id].ox
        ,r_data[emp_id].res);
    }
    
    function readGeneralRecord(string emp_id) public view returns(string[], string[]) {
        return (r_data[emp_id].steps, r_data[emp_id].create);
    }
}