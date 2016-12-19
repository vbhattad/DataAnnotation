import tensorflow as tf, sys

def getScore(image):

	image_path = image

	image_data = open(image_path, 'rb').read() #Read image data

	#Load label file
	label_lines = [line.rstrip() for line in open("tf_files/retrained_labels.txt")]

	# unpersists graph from file

	with open("tf_files/retrained_graph.pb",'rb') as f:
		graph_def = tf.GraphDef()
		graph_def.ParseFromString(f.read())
		_ = tf.import_graph_def(graph_def, name='')

	with tf.Session() as sess:
		softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
		
		predictions = sess.run(softmax_tensor, \
						{'DecodeJpeg/contents:0':image_data})
						
		top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
		score = 1.0
		returnvar = ""
		for node_id in top_k:
			human_String = label_lines[node_id]
			score = predictions[0][node_id]
			if score > 0.8:
				returnvar =  label_lines[node_id]
				
				#print('%s (score = %.5f)' % (human_String, score))
	return returnvar