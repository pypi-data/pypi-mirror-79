import scipy.sparse as ssp
import numpy as np
import bisect as bst
import csv











class RuleVectorMatrix():


	def __init__( self, n_features = None, n_classes = None, feature_names = None, feature_values_min = None, feature_values_max = None, class_names = None, predicate_type = 'range', file = None, verbose = 0 ):


		if ( n_features is None ) and ( n_classes is None ) and  ( file is None ): raise ValueError('( n_features , n_classes )  or ( file ) must be given.')


		self._verbose = verbose
		
		
		if file is not None:

			self.load_rules_matrix( file )
			self.n_rules_ = self.rules_matrix_.shape[ 0 ]


			if self.predicate_type_ == 'range':
				self._shift = 2
			elif self.predicate_type_ == 'binary':
				self._shift = 1


			self.__set_matrix_indexes()

		else:

			self.n_rules_ = 0

			self.features_used_ = [] # after filled, convert to np.array

			self.predicate_type_ = predicate_type
			if self.predicate_type_ == 'range':
				self._shift = 2
			elif self.predicate_type_ == 'binary':
				self._shift = 1


			if ( n_features is not None ) and ( n_classes is not None ):

				self.n_features_ = n_features

				if feature_names is None: self.feature_names_ = [ 'feature ' + str( f ) for f in range( 0, self.n_features_ ) ]
				else: self.feature_names_ = feature_names

				if feature_values_min is not None: self.feature_values_min_ = feature_values_min
				if feature_values_max is not None: self.feature_values_max_ = feature_values_max


				self.n_classes_ = n_classes

				if class_names is None:	self.class_names_ = [ 'class ' + str( c ) for c in range( 0, self.n_classes_ ) ]
				else: self.class_names_ = class_names

				self.__set_matrix_indexes()











	def __set_matrix_indexes( self ):


		self._rule_info = [ 'id', 'model', 'node', 'class', 'cover', 'certainty', 'n_predicates', 'ranges_diameter_mean', 'aux_1', 'aux_2', 'aux_3', 'value_total', 'value_c0' ]

		
		self.i_id = ( self.n_features_ * self._shift ) + self._rule_info.index( 'id' )
		self.i_model = ( self.n_features_ * self._shift ) + self._rule_info.index( 'model' )
		self.i_node = ( self.n_features_ * self._shift ) + self._rule_info.index( 'node' )
		
		self.i_class = ( self.n_features_ * self._shift ) + self._rule_info.index( 'class' )
		self.i_cover = ( self.n_features_ * self._shift ) + self._rule_info.index( 'cover' )
		self.i_certainty = ( self.n_features_ * self._shift ) + self._rule_info.index( 'certainty' )
		
		self.i_n_predicates = ( self.n_features_ * self._shift ) + self._rule_info.index( 'n_predicates' )
		self.i_ranges_diameter_mean = ( self.n_features_ * self._shift ) + self._rule_info.index( 'ranges_diameter_mean' )

		self.i_aux_1 = ( self.n_features_ * self._shift ) + self._rule_info.index( 'aux_1' )
		self.i_aux_2 = ( self.n_features_ * self._shift ) + self._rule_info.index( 'aux_2' )
		self.i_aux_3 = ( self.n_features_ * self._shift ) + self._rule_info.index( 'aux_3' )

		self.i_value_total = ( self.n_features_ * self._shift ) + self._rule_info.index( 'value_total' )
		self.i_value_c0 = ( self.n_features_ * self._shift ) + self._rule_info.index( 'value_c0' )


		self.__n_rule_info = len( self._rule_info ) + self.n_classes_ - 1

		if self._verbose > 1: print( 'rule info', self._rule_info )











	def _get_empty_rule( self ):

		return [ 'NaN' ] * ( ( self.n_features_ * self._shift ) + self.__n_rule_info )










	def print_rule( self, rule ):

		print( '---' )

		print( 'rule info ::' )


		print( 'id : ' + str( self.rules_matrix_[ rule, self.i_id ] ) )
		print( 'tree : ' + str( self.rules_matrix_[ rule, self.i_model ] ) )
		print( 'node : ' + str( self.rules_matrix_[ rule, self.i_node ] ) )
		
		print( 'class : ' + self.class_names_[ int( self.rules_matrix_[ rule, self.i_class ] ) ] )
		print( 'cover : ' + str( self.rules_matrix_[ rule, self.i_cover ] ) )
		print( 'certainty : ' + str( self.rules_matrix_[ rule, self.i_certainty ] ) )
		
		print( 'predicates : ' + str( self.rules_matrix_[ rule, self.i_n_predicates ] ) )
		print( 'ranges_diameter_mean : ' + str( self.rules_matrix_[ rule, self.i_ranges_diameter_mean ] ) )

		print( 'aux_1 : ' + str( self.rules_matrix_[ rule, self.i_aux_1 ] ) )
		print( 'aux_2 : ' + str( self.rules_matrix_[ rule, self.i_aux_2 ] ) )
		print( 'aux_3 : ' + str( self.rules_matrix_[ rule, self.i_aux_3 ] ) )
		
		print( 'prob : ' + str( self.rules_matrix_[ rule, self.i_value_c0: ].toarray()[ 0 ] / self.rules_matrix_[ rule, self.i_value_total ] ) )

		print( '---' )

		print( 'rule predicates ::' )

		f_printed = -1
		for f in self.rules_matrix_[ rule, :( self.n_features_ * self._shift ) ].nonzero()[ 1 ]:

			f = self._feature_map( f )

			if f != f_printed:
				f_printed = f

				a = f * 2
				b = a + 1
				print( 'f ' + str( f ) + ' : ' + self.feature_names_[ f ] + ' : [ ' + str( self.rules_matrix_[ rule, a ] ) + ', ' + str( self.rules_matrix_[ rule, b ] ) + ' ]' )

		print( '---' )











	def _insert_rule( self, rule_vector ):
		

		if self.rules_matrix_ is None:

			self.rules_matrix_ = ssp.lil_matrix( [ rule_vector ] )

		else:

			self.rules_matrix_ = ssp.vstack( [ self.rules_matrix_, rule_vector ], format = 'lil' ) # takes to much time to run ??

		self.n_rules_ += 1











	def _set_rules_matrix( self, rules_matrix ):

		self.rules_matrix_ = ssp.lil_matrix( rules_matrix )
		
		self.n_rules_ = self.rules_matrix_.shape[ 0 ]











	def apply_rule( self, rule, x_k, y_k = None, all_predicates = True ):

		x_k = self._check_input( x_k )


		result = 1

		f_checked = -1

		delta_sum = 0

		for f in self.rules_matrix_[ rule, :( self.n_features_ * self._shift ) ].nonzero()[ 1 ]:

			f = self._feature_map( f )

			if f != f_checked:
				f_checked = f

				predicate, delta = self.__apply_rule_predicate( rule, f, x_k[ f ] )

				if predicate == False:

					result = 0

					if all_predicates: delta_sum += delta # check all predicates for delta_sum to turn True the rule
					else: break # dot not check all predicates if at least one is False


		if ( ( y_k is not None ) and ( result == 1 ) and ( y_k != self.rules_matrix_[ rule, self.i_class ] ) ):
			result = -1

		if all_predicates: return result, delta_sum
		else: return result










	def _feature_map( self, f_ab ):

		if self.predicate_type_ == 'range':

			return int( f_ab / 2 )

		elif self.predicate_type_ == 'binary':

			return int( f_ab )











	def __apply_rule_predicate( self, rule, f, x_k_f ):

		result = False
		delta = 0

		if self.predicate_type_ == 'range':

			a = f * 2
			b = a + 1

			alpha = self.rules_matrix_[ rule, a ]
			beta = self.rules_matrix_[ rule, b ]

			if ( ( x_k_f >= alpha ) and ( x_k_f <= beta ) ):

				result = True

			else:

				if ( x_k_f < alpha ):

					delta = abs( x_k_f - alpha )

				else:

					delta = abs( x_k_f - beta )

				delta /= ( self.feature_values_max_[ f ] - self.feature_values_min_[ f ] )					

		elif self.predicate_type_ == 'binary':

			pass

		return result, delta











	def predict( self, X, **kwargs ):

		X = self._check_input( X )


		predictions = []
		predictions_proba = []

		list_id_result = []


		for k in range( X.shape[ 0 ] ):

			if self._verbose > 0: print( 'precting instance: ', k )

			y_predicted, proba, ids = self.predict_x( X[ k, : ], **kwargs )

			predictions.append( y_predicted )
			predictions_proba.append( proba )

			list_id_result.append( ids )


		return np.array( predictions ), np.array( predictions_proba ), np.array( list_id_result )











	def predict_x( self, x_k, by_model = True, closest_rules = False, list_id = 'id', counterfactual_class = 'first'  ):

		x_k = self._check_input( x_k )


		if by_model:

			if not closest_rules: model = -1
			else: model = 0


			voting = ssp.lil_matrix( ( 1, self.n_classes_ ) )
			list_id_result_1 = []

			
			# used when closest_rules == True
			list_id_result_2 = []
			rules_delta_sum = []

			rules = []
			rules_class = []
			rules_delta = []


			for rule in range( self.n_rules_ ):

				if not closest_rules: 

					if( self.rules_matrix_[ rule, self.i_model ] != model ):

						if self._verbose > 1: print( 'applying instance on rule: ', rule )

						result = self.apply_rule( rule, x_k, all_predicates = False )

						if result == 1:

							model = self.rules_matrix_[ rule, self.i_model ]

							if list_id == 'id': list_id_result_1.append( rule ) # ??
							elif list_id == 'model': list_id_result_1.append( self.rules_matrix_[ rule, self.i_model ].astype( int ) ) 
							elif list_id == 'node': list_id_result_1.append( self.rules_matrix_[ rule, self.i_node ].astype( int ) )

							voting += ( self.rules_matrix_[ rule, self.i_value_c0: ] / self.rules_matrix_[ rule, self.i_value_total ] )

				else:

					if self._verbose > 1: print( 'applying instance on rule: ', rule )

					result, delta_sum = self.apply_rule( rule, x_k )
					rules_delta_sum.append( delta_sum )


					if( self.rules_matrix_[ rule, self.i_model ] != model ):

						closest = self.__get_closest_rule( rule_true_class, rules, rules_class, counterfactual_class )

						if counterfactual_class == 'first': 

							if list_id == 'id': list_id_result_2.append( closest ) # ??
							elif list_id == 'model': list_id_result_2.append( self.rules_matrix_[ closest, self.i_model ].astype( int ) )
							elif list_id == 'node': list_id_result_2.append( self.rules_matrix_[ closest, self.i_node ].astype( int ) )

						elif counterfactual_class == 'all':

							if list_id == 'id': list_id_result_2.extend( closest )
							elif list_id == 'model': list_id_result_2.extend( self.rules_matrix_[ closest, self.i_model ].astype( int ).tolist() )
							elif list_id == 'node': list_id_result_2.extend( self.rules_matrix_[ closest, self.i_node ].astype( int ).tolist() )


						model = self.rules_matrix_[ rule, self.i_model ]

						rules = []
						rules_class = []
						rules_delta = []


					if result == 1:

						rule_true_class = self.rules_matrix_[ rule, self.i_class ].astype( int )

						if list_id == 'id': list_id_result_1.append( rule ) # ??
						elif list_id == 'model': list_id_result_1.append( self.rules_matrix_[ rule, self.i_model ].astype( int ) )
						elif list_id == 'node': list_id_result_1.append( self.rules_matrix_[ rule, self.i_node ].astype( int ) )

						voting += ( self.rules_matrix_[ rule, self.i_value_c0: ] / self.rules_matrix_[ rule, self.i_value_total ] )

					else:

						index = bst.bisect_left( rules_delta, delta_sum )
						rules_delta.insert( index, delta_sum )
						rules.insert( index, rule )
						rules_class.insert( index, self.rules_matrix_[ rule, self.i_class ].astype( int ) )				

			
			if closest_rules: # last model didn't check by ' if( self.rules_matrix_[ rule, self.i_model ] != model ): '

				closest = self.__get_closest_rule( rule_true_class, rules, rules_class, counterfactual_class )

				if counterfactual_class == 'first': 

					if list_id == 'id': list_id_result_2.append( closest ) # ??
					elif list_id == 'model': list_id_result_2.append( self.rules_matrix_[ closest, self.i_model ].astype( int ) )
					elif list_id == 'node': list_id_result_2.append( self.rules_matrix_[ closest, self.i_node ].astype( int ) )

				elif counterfactual_class == 'all':

					if list_id == 'id': list_id_result_2.extend( closest )
					elif list_id == 'model': list_id_result_2.extend( self.rules_matrix_[ closest, self.i_model ].astype( int ).tolist() )
					elif list_id == 'node': list_id_result_2.extend( self.rules_matrix_[ closest, self.i_node ].astype( int ).tolist() )



			voting = voting.toarray()[ 0 ]

			proba = voting / voting.sum()
			y_predicted = np.argmax( proba )


		if closest_rules: return y_predicted, proba, np.array( list_id_result_1 ), np.array( list_id_result_2 ), np.array( rules_delta_sum )
		else: return y_predicted, proba, np.array( list_id_result_1 )











	def __get_closest_rule( self, rule_true_class, rules, rules_class, counterfactual_class = 'first' ): # 'rules' and 'rules_class' sorted by rules_delta

		if counterfactual_class == 'first': 

			for i in range( len( rules ) ): 

				if rule_true_class != rules_class[ i ]: return rules[ i ]

		elif counterfactual_class == 'all':

			r_list = []
			r_list_classes = []
			r_list_classes.append( rule_true_class )

			for i in range( len( rules ) ): 

				if ( rules_class[ i ] not in r_list_classes  ): 

					r_list.append( rules[ i ] )
					r_list_classes.append( rules_class[ i ] )

			return r_list













	def _aggregate_voting( self, rules, partial = True ): # by rows above

		n_rules = rules.shape[ 0 ]

		certainty = self.rules_matrix_[ rules, self.i_value_c0: ].toarray() / self.rules_matrix_[ rules, self.i_value_total ].toarray()

		if partial:

			partial_voting = []

			partial_voting.append( certainty[ 0 ] )

			for r in range( n_rules ):

				if r != 0:
					voting = np.sum( certainty[ 0:( r + 1 ) ], axis = 0 )
					partial_voting.append( voting / voting.sum() )


			return np.array( partial_voting )

		else:

			voting = np.sum( certainty, axis = 0 )
			return voting / voting.sum()



		







	def _get_features_used( self, rules ):


		features_ab = np.unique( self.rules_matrix_[ rules, :( self.n_features_ * self._shift ) ].nonzero()[ 1 ] )

		features_used = []

		for f_ab in features_ab:

			f = self._feature_map( f_ab )

			if f not in features_used: features_used.append( f )

		return np.array( features_used )











	def _to_features_ab( self, features ):

		features_used_ab = []

		for f in features:

			a = f * 2
			b = a + 1

			features_used_ab.append( a )
			features_used_ab.append( b )

		return features_used_ab











	def _check_input( self, X ):

		if X.dtype == np.float32: return X
		else:  return np.asfortranarray( X, dtype = np.float32 )











	def save_rules_matrix( self, file ):

		try:


			if self._verbose > 0: print( 'saving rules_matrix_ ...' )

			with open( file + '.csv', 'w', encoding = 'utf-8' ) as csv_file:

				writer = csv.writer( csv_file, delimiter = ';' )

				writer.writerow( [ 'n_features_, n_classes_, predicate_type_' ] )
				writer.writerow( [ self.n_features_, self.n_classes_, self.predicate_type_ ] )
				writer.writerow( [ 'feature_names_'] )
				writer.writerow( self.feature_names_ )
				writer.writerow( [ 'feature_values_min_' ] )
				writer.writerow( self.feature_values_min_ )
				writer.writerow( [ 'feature_values_max_' ] )
				writer.writerow( self.feature_values_max_ )
				writer.writerow( [ 'features_used_' ] )
				writer.writerow( self.features_used_ )
				writer.writerow( [ 'feature_importances_' ] )
				writer.writerow( self.feature_importances_ )
				writer.writerow( [ 'class_names_' ] )
				writer.writerow( self.class_names_ )

				
				header = []
				for f in range( self.n_features_ ):
					header.append( self.feature_names_[ f ] + ' alpha ' )
					header.append( self.feature_names_[ f ] + ' beta ' )
				header.extend( self._rule_info )
				for c in range( self.n_classes_ - 1 ):
					header.append( 'value_c' + str( c + 1 ) )

				writer.writerow( header )

				
				writer.writerows( self.rules_matrix_.toarray() )

				
				csv_file.close()

			if self._verbose > 0: print( 'rules_matrix_ saved' )


		except Exception as e:
			print( e )









			

	def load_rules_matrix( self, file ):

		try:


			metadata = np.loadtxt( file + '.csv', delimiter = ';', skiprows = 1, max_rows = 1, dtype = 'str' )
			self.n_features_ = int( metadata[ 0 ] )
			self.n_classes_ = int( metadata[ 1 ] )
			self.predicate_type_ = metadata[ 2 ]
			if self._verbose > 0: print( 'n_features loaded', self.n_features_ )
			if self._verbose > 0: print( 'n_classes loaded', self.n_classes_ )
			if self._verbose > 0: print( 'predicate_type loaded', self.predicate_type_ )


			self.feature_names_ = np.loadtxt( file + '.csv', delimiter = ';', skiprows = 3, max_rows = 1, dtype = 'str' )
			if self._verbose > 0: print( 'feature_names loaded', self.feature_names_.shape )


			self.feature_values_min_ = np.loadtxt( file + '.csv', delimiter = ';', skiprows = 5, max_rows = 1 )
			if self._verbose > 0: print( 'feature_values_min loaded', self.feature_values_min_.shape )

			
			self.feature_values_max_ = np.loadtxt( file + '.csv', delimiter = ';', skiprows = 7, max_rows = 1 )
			if self._verbose > 0: print( 'feature_values_max loaded', self.feature_values_max_.shape )

			
			self.features_used_ = np.loadtxt( file + '.csv', delimiter = ';', skiprows = 9, max_rows = 1, dtype = 'int' )
			if self._verbose > 0: print( 'features_used loaded', self.features_used_.shape )


			self.feature_importances_ = np.loadtxt( file + '.csv', delimiter = ';', skiprows = 11, max_rows = 1 )
			if self._verbose > 0: print( 'eature_importances loaded', self.feature_importances_.shape )
			

			self.class_names_ = np.loadtxt( file + '.csv', delimiter = ';', skiprows = 13, max_rows = 1, dtype = 'str' )
			if self._verbose > 0: print( 'class_names loaded', self.class_names_.shape )


			if self._verbose > 0: print( 'loading rules_matrix_ ...' )
			self.rules_matrix_ = ssp.lil_matrix( np.loadtxt( file + '.csv', delimiter = ';', skiprows = 15 ) )
			if self._verbose > 0: print( 'rules_matrix_ loaded ', self.rules_matrix_.shape )


		except Exception as e:
			print( e )