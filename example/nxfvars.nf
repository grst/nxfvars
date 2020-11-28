import groovy.json.JsonBuilder

def nxfVars(task) {
    // get rid of `$` variable and `task`. We'll cover the latter separately. 
    def tmp_inputs = task.binding.findAll { 
        it.key != '$' && it.key != 'task' 
    }
    def tmp_task = task.binding.task.each { it }
    def tmp_params = this.binding.variables['params']

    // convert all agruments to Strings
    // otherwise it can't be converted to json and
    // I currently don't see why we would need a higher nesting level. 
    def nxf_vars = [input: tmp_inputs, task: tmp_task, params: tmp_params].collectEntries {
        [it.key, it.value.collectEntries {
            [it.key, it.value.toString()]
        }]
    }

    // convert to json
    def builder = new JsonBuilder()
    builder(nxf_vars)

    // convert to base 64 string
    def nxf_vars_b64 = builder.toString().bytes.encodeBase64().toString()

    // Generate a line that can be added to the bash script. 
    "export NXF_VARS=\"${nxf_vars_b64}\""
}